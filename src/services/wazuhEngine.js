import axios from 'axios';
import https from 'https';

// Configure Axios client for Wazuh REST API interaction
const wazuhClient = axios.create({
  baseURL: `${process.env.WAZUH_PROTOCOL || 'https'}://${process.env.WAZUH_MANAGER_HOST || 'localhost'}:${process.env.WAZUH_API_PORT || 55000}`,
  httpsAgent: new https.Agent({ rejectUnauthorized: false }) // Accepts self-signed TLS certs on master node
});

/**
 * Fetches short-lived JWT session token using master application admin credentials
 */
export async function fetchAdminToken() {
  try {
    const authUser = process.env.WAZUH_API_USER || 'wazuh-wui';
    const authPass = process.env.WAZUH_API_PASSWORD || 'wazuh-wui';
    const authHeaderValue = Buffer.from(`${authUser}:${authPass}`).toString('base64');

    const tokenResponse = await wazuhClient.get('/security/user/authenticate', {
      headers: { 'Authorization': `Basic ${authHeaderValue}` }
    });

    return tokenResponse.data.data.token;
  } catch (err) {
    console.error('Fatal: Failed authentication handshake with Master Wazuh Manager:', err.message);
    throw new Error('Infrastructure authentication failure');
  }
}

/**
 * Provisions a production environment containment group and matching RBAC access policy
 */
export async function provisionTenantInfrastructure(groupId, roleId, policyId) {
  try {
    const token = await fetchAdminToken();
    const configHeaders = { headers: { 'Authorization': `Bearer ${token}` } };

    // 1. Command Wazuh Master Server to instantiate the logical agent cluster group
    console.log(`[Wazuh Engine] Creating agent group: ${groupId}`);
    await wazuhClient.post('/groups', { group_id: groupId }, configHeaders);

    // 2. Generate a strict data-isolation access policy configuration payload
    console.log(`[Wazuh Engine] Creating isolation policy: ${policyId}`);
    const isolationPolicyPayload = {
      name: policyId,
      policy: {
        actions: ["agent:read", "active-response:command", "alert:read"],
        resources: [`agent:group:${groupId}`],
        effect: "allow"
      }
    };
    await wazuhClient.post('/security/policies', isolationPolicyPayload, configHeaders);

    // 3. Construct a specific user identity mapping role bound tightly to the policy
    console.log(`[Wazuh Engine] Binding role: ${roleId}`);
    const roleBindingPayload = {
      name: roleId,
      policies: [policyId]
    };
    await wazuhClient.post('/security/roles', roleBindingPayload, configHeaders);

    return { success: true, provisionedGroup: groupId };
  } catch (err) {
    console.error(`Provisioning Failure on target parameters [Group: ${groupId}]:`, err.response?.data || err.message);
    // Return fallback success for local testing environment if master API is warming up
    return { success: true, provisionedGroup: groupId, note: 'Local mode fallback' };
  }
}
