import express from 'express';
import { PrismaClient } from '@prisma/client';
import { scriptDeliveryLimiter } from '../middlewares/rateLimiter.js';

const prisma = new PrismaClient();
const router = express.Router();

// Apply rate limiter (Max 60 requests / hour per IP)
router.use('/deployment-script', scriptDeliveryLimiter);

// Middleware placeholder for JWT authentication verification
const checkJwtAuthHeader = (req, res, next) => {
  req.authenticatedUser = req.user || { id: "demo-user-id" };
  next();
};

router.get('/deployment-script', checkJwtAuthHeader, async (req, res) => {
  try {
    const databaseUserProfile = await prisma.user.findUnique({
      where: { id: req.authenticatedUser.id }
    });

    if (!databaseUserProfile || databaseUserProfile.paymentStatus !== 'active' || !databaseUserProfile.wazuhGroupId) {
      return res.status(403).json({ error: 'Access Denied: Verifiable, active commercial enterprise account required.' });
    }

    const wazuhHost = process.env.WAZUH_MANAGER_HOST || 'localhost';

    const targetedInstallationString = `curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | gpg --dearmor -o /usr/share/keyrings/wazuh.gpg && echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | tee /etc/apt/sources.list.d/wazuh.list && apt-get update && WAZUH_MANAGER="${wazuhHost}" WAZUH_AGENT_GROUP="${databaseUserProfile.wazuhGroupId}" apt-get install wazuh-agent -y && sudo systemctl daemon-reload && sudo systemctl enable wazuh-agent && sudo systemctl start wazuh-agent`;

    return res.status(200).json({
      allocatedGroupSilo: databaseUserProfile.wazuhGroupId,
      targetExecutionCommand: targetedInstallationString
    });

  } catch (runtimeCommandGenerationError) {
    console.error('Error serving orchestration string:', runtimeCommandGenerationError);
    return res.status(500).json({ error: 'Failed to synthesize target custom onboarding environment configurations' });
  }
});

export default router;
