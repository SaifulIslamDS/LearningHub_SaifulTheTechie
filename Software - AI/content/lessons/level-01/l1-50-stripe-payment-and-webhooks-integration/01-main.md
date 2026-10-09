---
title: Integrate Stripe Checkout & Reliable Webhooks
order: 1
summary: Understand the payment lifecycle, create Checkout Sessions, verify webhook events and store idempotent payment records.
level: Intermediate
time: 100–140 min
curriculum_level: Level 01
source_module: '50'
source_type: source-curriculum
topics:
- 'Introduction to Stripe: Payment Flow and Architecture Overview'
- 'Stripe Setup: API Keys, Products, and Pricing Configuration'
- Implementing Stripe Checkout Session in Next.js
- Payment Success and Cancel Page Handling
- 'Introduction to Stripe Webhooks: Events and Listeners'
- Setting Up Webhook Endpoint in Express Backend
- 'Handling Webhook Events: Payment Success, Failure, and'
- Securing Webhook Endpoint with Stripe Signature Verification
- Storing Payment Records in MongoDB
- Testing Payment Flow End-to-End in Stripe Test Mode
prerequisites:
- level-01/l1-49-core-implementation/01-main
keywords:
- stripe
- checkout
- webhook
- signature
- payment
- idempotency
reviewed: '2026-10-09'
files:
- level-01/fullstack-project-1-blueprint.zip
- level-01/backend-mongodb-practice.zip
resources:
- title: Stripe Checkout quickstarts
  url: https://docs.stripe.com/payments/checkout/quickstarts
  source: Stripe
  note: Official Checkout Sessions quickstarts.
- title: Webhook endpoints
  url: https://docs.stripe.com/api/webhook_endpoints
  source: Stripe
  note: Official webhook endpoint API reference.
- title: Stripe documentation
  url: https://docs.stripe.com/
  source: Stripe
  note: Official payment integration documentation.
youtube:
  title: How to Accept Payments with Stripe and Express
  creator: WittCode
  url: https://www.youtube.com/watch?v=zP9TnSJHkOE
  video_id: zP9TnSJHkOE
  duration: ≈18 min
  language: English
  level: Intermediate
  reviewed: '2026-10-09'
  why_recommended: A compact visual companion for Stripe Checkout sessions and webhook handling with Express. Stripe official documentation remains the authority for security-sensitive and version-sensitive implementation details.
  timestamps:
  - label: Checkout session
    time: 07:40
  - label: Webhooks
    time: 09:16
  - label: Webhook with Express
    time: '13:06'
  - label: Successful payment event
    time: '15:09'
---
## Start here

A payment redirect is not proof that money was successfully processed. Payment systems are asynchronous and can deliver events after the browser has closed.

Use this mental model:

```text
browser asks your server to start checkout
      ↓
your server creates Stripe Checkout Session
      ↓
browser completes hosted checkout
      ↓
Stripe sends webhook to your backend
      ↓
backend verifies signature + records payment result
      ↓
application grants/updates entitlement
```

The webhook is the critical server-to-server confirmation path.

## What you will learn

- Stripe payment architecture;
- API keys/products/prices as server configuration;
- creating a Checkout Session;
- success/cancel browser routes;
- webhook purpose;
- Express webhook endpoint concept;
- handling success/failure/refund-style events;
- signature verification;
- storing payment records;
- testing end-to-end in Stripe test mode.

## 1. Keep the secret key on the server

The backend uses the secret API key. Never expose it through `NEXT_PUBLIC_*`, bundle it into client JavaScript or commit it.

```text
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

## 2. Create a Checkout Session

Reference-only server snippet:

```js
const session = await stripe.checkout.sessions.create({
  mode: "payment",
  line_items: [{ price: process.env.STRIPE_PRICE_ID, quantity: 1 }],
  success_url: `${APP_URL}/success`,
  cancel_url: `${APP_URL}/cancel`,
});
```

Return the session URL/identifier to the browser and redirect to Stripe's hosted checkout.

## 3. Success page is UX, not payment authority

A user can open a URL directly. Do not mark an order paid just because `/success` rendered.

The reliable source is a verified server event from Stripe.

## 4. Webhook endpoint

The webhook receives event payloads from Stripe. Signature verification proves that the payload matches what Stripe signed using your endpoint secret.

Conceptual Express flow:

```text
POST /webhooks/stripe
  ↓ raw request body
construct/verify event signature
  ↓
switch event.type
  ↓
update application payment/order state
  ↓
return 2xx promptly
```

Follow current Stripe documentation carefully because middleware/body parsing configuration matters for signature verification.

## 5. Make event handling idempotent

Stripe may retry events. Your handler should not create duplicate purchases every time the same event ID arrives.

The bundled `run/05_payment_record.mjs` demonstrates the principle:

<span class="output-label">Verified output</span>

```text
stored
duplicate ignored
records=1
```

In production, store the provider event ID with a uniqueness guarantee or equivalent durable idempotency mechanism.

## 6. Store payment records separately from UI state

A payment record might contain:

```text
providerEventId
checkoutSessionId
userId
product/serviceId
amount
currency
status
createdAt
```

Keep enough information to reconcile support issues without storing unnecessary sensitive payment data.

## 7. Failure and refund events

Do not design only `payment_succeeded`. A robust model understands failed, expired, refunded or disputed states according to the product's needs.

Map external provider states into your own small domain vocabulary where useful.

## 8. Test mode checklist

When you have a Stripe test account:

1. create a test Checkout Session;
2. complete it with a Stripe test payment method;
3. observe the webhook event;
4. confirm signature verification;
5. confirm one payment record;
6. resend the same event and confirm no duplicate entitlement;
7. test cancel/failure behavior.

Stripe packages and account calls were not available in the release environment, so checkout/webhook code is **REFERENCE-ONLY**. Only the idempotency demonstration above was executed locally; its output is real.
