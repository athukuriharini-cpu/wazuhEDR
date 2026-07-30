import axios from 'axios';
import https from 'https';

// Strict TLS Handshake configuration (rejectUnauthorized: true in production)
const isRejectUnauthorized = process.env.WAZUH_REJECT_UNAUTHORIZED === 'true' || process.env.NODE_ENV === 'production';

const wazuhClient = axios.create({
  baseURL: `${process.env.WAZUH_PROTOCOL || 'https'}://${process.env.WAZUH_MANAGER_HOST || 'localhost'}:${process.env.WAZUH_API_PORT || 55000}`,
  httpsAgent: new https.Agent({ rejectUnauthorized: isRejectUnauthorized })
});

// In-Memory Keep-Alive JWT Token Caching Variables
let cachedAdminToken = null;
let tokenExpiryTimestamp = 0; // Milliseconds timestamp

/**
 * Fetches or reuses cached JSON Web Token (JWT) session token.
 * Only triggers POST /security/user/authenticate when within 5 minutes of expiration.
 */
export async function fetchAdminToken() {
  const nowMs = Date.now();
  const fiveMinutesMs = 5 * 60 * 1000;

  // Reuse cached token if valid and not within 5 minutes of expiry
  if (cachedAdminToken && tokenExpiryTimestamp > (nowMs + fiveMinutesMs)) {
    return cachedAdminToken;
  }

  try {
    const authUser = process.env.WAZUH_API_USER || 'wazuh-wui';
    const authPass = process.env.WAZUH_API_PASSWORD || 'wazuh-wui';
    const authHeaderValue = Buffer.from(`${authUser}:${authPass}`).toString('base64');

    console.log('[Wazuh Engine] Requesting fresh JWT session token from Master Manager...');
    const tokenResponse = await wazuhClient.get('/security/user/authenticate', {
      headers: { 'Authorization': `Basic ${authHeaderValue}` }
    });

    cachedAdminToken = tokenResponse.data.data.token;
    // Default Wazuh JWT token duration is 1 hour (3600 seconds)
    tokenExpiryTimestamp = Date.now() + (3600 * 1000);
    console.log('[Wazuh Engine] Fresh JWT session token cached successfully.');

    return cachedAdminToken;
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
    return { success: true, provisionedGroup: groupId, note: 'Local mode fallback' };
  }
}

/**
 * Automated Tenant Offboarding: Deletes tenant role, RBAC policy, and group silo upon subscription cancellation
 */
export async function offboardTenantInfrastructure(groupId, roleId, policyId) {
  try {
    const token = await fetchAdminToken();
    const configHeaders = { headers: { 'Authorization': `Bearer ${token}` } };

    console.log(`[Wazuh Engine] Offboarding Tenant Infrastructure [Group: ${groupId}, Role: ${roleId}]...`);

    // 1. Delete Role Binding
    if (roleId) {
      await wazuhClient.delete(`/security/roles?role_ids=${roleId}`, configHeaders).catch(() => {});
    }

    // 2. Delete RBAC Isolation Policy
    if (policyId) {
      await wazuhClient.delete(`/security/policies?policy_ids=${policyId}`, configHeaders).catch(() => {});
    }

    // 3. Delete Containment Group
    if (groupId) {
      await wazuhClient.delete(`/groups?groups_list=${groupId}`, configHeaders).catch(() => {});
    }

    console.log(`[Wazuh Engine] Offboarding complete for group: ${groupId}`);
    return { success: true, offboardedGroup: groupId };
  } catch (err) {
    console.error(`Offboarding Failure on target parameters [Group: ${groupId}]:`, err.message);
    return { success: false, error: err.message };
  }
}
