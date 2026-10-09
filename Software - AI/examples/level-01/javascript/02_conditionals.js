const orderTotal = 1800;
const isMember = true;
let shipping;
if (orderTotal >= 2000) shipping = 0;
else if (isMember) shipping = 60;
else shipping = 120;
console.log(`Shipping charge: BDT ${shipping}`);
console.log(orderTotal + shipping <= 1900 ? "Within budget" : "Over budget");
