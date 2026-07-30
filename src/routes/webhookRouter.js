import express from 'express';
import Stripe from 'stripe';
import { PrismaClient } from '@prisma/client';
import { provisionTenantInfrastructure, offboardTenantInfrastructure } from '../services/wazuhEngine.js';
import { webhookLimiter } from '../middlewares/rateLimiter.js';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || 'sk_test_mock');
const prisma = new PrismaClient();
const router = express.Router();

// Apply aggressive rate limiter (Max 5 attempts / minute per IP)
router.use('/stripe', webhookLimiter);

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

  // 1. Intercept explicit completed checkout sessions (ONBOARDING)
  if (verifiedEvent.type === 'checkout.session.completed') {
    const activeSessionObject = verifiedEvent.data.object;
    const clientCustomerEmail = activeSessionObject.customer_details?.email || activeSessionObject.customer_email;

    if (!clientCustomerEmail) {
      return res.status(400).send('Missing critical email profile inside payment context metadata');
    }

    const generationToken = Math.random().toString(36).substring(2, 11);
    const tenantGroupId = `grp_${generationToken}`;
    const tenantRoleId = `role_${generationToken}`;
    const tenantPolicyId = `policy_${generationToken}`;

    try {
      await prisma.$transaction(async (transactionEngine) => {
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

        await provisionTenantInfrastructure(tenantGroupId, tenantRoleId, tenantPolicyId);
      });

      console.log(`Success: Multi-tenant container layer fully operational for user account: ${clientCustomerEmail}`);
    } catch (transactionCrashError) {
      console.error(`Critical Error: Onboarding Pipeline Failure for account ${clientCustomerEmail}:`, transactionCrashError);
      return res.status(500).send('Internal infrastructure alignment crash');
    }
  }

  // 2. Intercept canceled or deleted subscriptions (OFFBOARDING)
  if (verifiedEvent.type === 'customer.subscription.deleted' || verifiedEvent.type === 'customer.subscription.updated') {
    const subObject = verifiedEvent.data.object;

    if (subObject.status === 'canceled' || subObject.status === 'unpaid' || verifiedEvent.type === 'customer.subscription.deleted') {
      try {
        const tenantUser = await prisma.user.findFirst({
          where: { stripeCustomerId: subObject.customer }
        });

        if (tenantUser && tenantUser.wazuhGroupId) {
          console.log(`[Stripe Webhook] Subscription Canceled/Deleted for customer: ${tenantUser.email}`);

          // Trigger Automated Offboarding in Master Wazuh Server
          await offboardTenantInfrastructure(tenantUser.wazuhGroupId, tenantUser.wazuhRoleId, tenantUser.wazuhPolicyId);

          // Update DB Status
          await prisma.user.update({
            where: { id: tenantUser.id },
            data: { paymentStatus: 'canceled' }
          });
        }
      } catch (offboardError) {
        console.error('Error executing automated offboarding pipeline:', offboardError.message);
      }
    }
  }

  // Acknowledge receipt of the webhook to prevent retry storms
  res.status(200).json({ received: true });
});

export default router;
