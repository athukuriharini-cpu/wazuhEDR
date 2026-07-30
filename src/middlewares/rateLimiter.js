import rateLimit from 'express-rate-limit';

/**
 * Aggressive rate-limiter for Stripe & Payment Webhook Endpoints
 * Production Metric: Restrict checkout creations to max 5 attempts per IP per minute
 */
export const webhookLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute window
  max: 5, // Limit each IP to 5 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: 'Too many payment webhook verification attempts from this IP. Please try again after 1 minute.'
  }
});

/**
 * Rate-limiter for Agent Onboarding Script Delivery Routes
 * Production Metric: Restrict dashboard script generations to max 60 requests per hour
 */
export const scriptDeliveryLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour window
  max: 60, // Limit each IP to 60 requests per hour
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: 'Rate limit exceeded: Maximum 60 script generation requests per hour permitted.'
  }
});
