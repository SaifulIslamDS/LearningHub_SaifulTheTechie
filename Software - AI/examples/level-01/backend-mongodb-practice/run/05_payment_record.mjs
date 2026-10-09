const payments=new Map();
function applyEvent(event){ if(payments.has(event.id)) return "duplicate ignored"; payments.set(event.id,{status:event.type,amount:event.amount}); return "stored"; }
const event={id:"evt_demo_001",type:"checkout.session.completed",amount:2500};
console.log(applyEvent(event)); console.log(applyEvent(event)); console.log(`records=${payments.size}`);
