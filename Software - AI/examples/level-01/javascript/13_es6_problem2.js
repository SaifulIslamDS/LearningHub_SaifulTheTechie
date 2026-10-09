const orders = [{customer:"A",amount:1200},{customer:"B",amount:900},{customer:"A",amount:800}];
const totals = orders.reduce((acc, order) => { acc[order.customer] = (acc[order.customer] ?? 0) + order.amount; return acc; }, {});
console.log(JSON.stringify(totals));
const winner = Object.entries(totals).sort((a,b) => b[1]-a[1])[0];
console.log(`Top customer: ${winner[0]} (${winner[1]})`);
