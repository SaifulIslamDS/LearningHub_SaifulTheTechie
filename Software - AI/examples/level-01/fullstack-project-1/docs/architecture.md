# Architecture

Browser / Next.js UI
        ↓ HTTPS
Next.js frontend ──────→ Express REST API
                            ↓
                        MongoDB
                            ↑
Stripe Checkout → Stripe webhook endpoint

Keep authorization in the API even when the UI hides controls. Treat the webhook as the source of truth for asynchronous payment completion.
