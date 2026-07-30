import { WebSocketServer, WebSocket } from 'ws';
import axios from 'axios';
import https from 'https';

const isRejectUnauthorized = process.env.WAZUH_REJECT_UNAUTHORIZED === 'true' || process.env.NODE_ENV === 'production';

const indexerClient = axios.create({
  baseURL: `https://${process.env.WAZUH_INDEXER_HOST || 'localhost'}:${process.env.WAZUH_INDEXER_PORT || 9200}`,
  auth: {
    username: process.env.WAZUH_INDEXER_USER || 'admin',
    password: process.env.WAZUH_INDEXER_PASS || 'admin'
  },
  httpsAgent: new https.Agent({ rejectUnauthorized: isRejectUnauthorized })
});

/**
 * Initializes Dynamic Alert WebSocket Server.
 * Polls OpenSearch Indexer for live security alerts matching tenant's wazuhGroupId
 * and streams real-time threat alerts directly to client dashboards.
 */
export function initWebSocketServer(server) {
  const wss = new WebSocketServer({ server, path: '/api/v1/ws/alerts' });

  console.log('[WebSocket Server] Live Alert Streamer initialized on /api/v1/ws/alerts');

  wss.on('connection', (ws, req) => {
    // Extract tenant group ID from query params e.g. /api/v1/ws/alerts?groupId=grp_01a2b3c4
    const urlParams = new URLSearchParams(req.url.split('?')[1]);
    const tenantGroupId = urlParams.get('groupId');

    if (!tenantGroupId) {
      ws.close(4001, 'Missing tenant groupId query parameter');
      return;
    }

    console.log(`[WebSocket Server] Client connected for isolated group: ${tenantGroupId}`);

    // Poll OpenSearch Indexer every 3 seconds for new alerts matching this tenant group
    const intervalId = setInterval(async () => {
      if (ws.readyState !== WebSocket.OPEN) return;

      try {
        const query = {
          size: 5,
          sort: [{ "@timestamp": { order: "desc" } }],
          query: {
            bool: {
              must: [
                { range: { "@timestamp": { gte: "now-30s" } } },
                { match: { "agent.group": tenantGroupId } }
              ]
            }
          }
        };

        const resp = await indexerClient.post('/wazuh-alerts*/_search', query).catch(() => null);

        if (resp && resp.data?.hits?.hits) {
          const alerts = resp.data.hits.hits.map(hit => hit._source);
          if (alerts.length > 0) {
            ws.send(JSON.stringify({ type: 'LIVE_ALERTS', groupId: tenantGroupId, alerts }));
          }
        }
      } catch (err) {
        // Silent catch for background poll
      }
    }, 3000);

    ws.on('close', () => {
      clearInterval(intervalId);
      console.log(`[WebSocket Server] Client disconnected for group: ${tenantGroupId}`);
    });
  });

  return wss;
}
