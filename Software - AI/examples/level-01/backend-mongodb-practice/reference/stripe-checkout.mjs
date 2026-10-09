// REFERENCE-ONLY: requires stripe and a Stripe test account.
import Stripe from "stripe";
const stripe=new Stripe(process.env.STRIPE_SECRET_KEY);
const session=await stripe.checkout.sessions.create({mode:"payment",line_items:[{price:process.env.STRIPE_PRICE_ID,quantity:1}],success_url:"http://localhost:3000/success",cancel_url:"http://localhost:3000/cancel"});
console.log(session.url);
