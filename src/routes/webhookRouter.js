import express from 'express';
import Stripe from 'stripe';
import { PrismaClient } from '@prisma/client';
import { provisionTenantInfrastructure } from '../services/wazuhEngine.js';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || 'sk_test_mock');
const prisma = new PrismaClient();
const router = express.Router();

router.post('/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const cryptographicSignature = req.headers['stripe-signature'];
  let verifiedEvent;

  try {
    // Prevent request spoofing by validating signature from Stripe production certificates
    if (process.env.STRIPE_WEBHOOK_SECRET) {
      verifiedEvent = stripe.webhooks.constructEvent(
        req.body,
        cryptographicSignature,
        process.env.STRIPE_WEBHOOK_SECRET
      );
    } else {
      // Development fallback parsing
      verifiedEvent = JSON.parse(req.body.toString());
    }
  } catch (signatureVerificationError) {
    console.error(`Security Warning: Rogue Webhook Attempt Blocked:`, signatureVerificationError.message);
    return res.status(400).send(`Webhook Signature Authentication Violated`);
  }

  // Intercept explicit completed transaction instances
  if (verifiedEvent.type === 'checkout.session.completed') {
    const activeSessionObject = verifiedEvent.data.object;
    const clientCustomerEmail = activeSessionObject.customer_details?.email || activeSessionObject.customer_email;

    if (!clientCustomerEmail) {
      return res.status(400).send('Missing critical email profile inside payment context metadata');
    }

    // Generate strict, unique asset tokens for database tracking and Wazuh definitions
    const generationToken = Math.random().toString(36).substring(2, 11);
    const tenantGroupId = `grp_${generationToken}`;
    const tenantRoleId = `role_${generationToken}`;
    const tenantPolicyId = `policy_${generationToken}`;

    try {
      // Execute multi-stage persistence operations as a single unit
      await prisma.$transaction(async (transactionEngine) => {
        // Upgrade system data status parameters indicating successful paid authorization
        await transactionEngine.user.update({
          where: { email: clientCustomerEmail },
          data: {
            stripeCustomerId: activeSessionObject.customer,
            paymentStatus: 'active',
            wazuhGroupId: tenantGroupId,
            wazuhRoleId: tenantRoleId,
            wazuhPolicyId: tenantPolicyId
          }
        });

        // Trigger remote API operations on the Master Wazuh instance
        await provisionTenantInfrastructure(tenantGroupId, tenantRoleId, tenantPolicyId);
      });

      console.log(`Success: Multi-tenant container layer fully operational for user account: ${clientCustomerEmail}`);
    } catch (transactionCrashError) {
      console.error(`Critical Error: Onboarding Pipeline Failure for account ${clientCustomerEmail}:`, transactionCrashError);
      return res.status(500).send('Internal infrastructure alignment crash');
    }
  }

  // Acknowledge receipt of the webhook to prevent retry storms
  res.status(200).json({ received: true });
});

export default router;
