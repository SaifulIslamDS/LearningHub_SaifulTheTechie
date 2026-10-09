const orders = [{id:1,status:"Delivered",amount:1200},{id:2,status:"Cancelled",amount:800},{id:3,status:"Delivered",amount:1500},{id:4,status:"Pending",amount:500}];
let deliveredRevenue = 0; let deliveredCount = 0;
for (const order of orders) { if (order.status !== "Delivered") continue; deliveredRevenue += order.amount; deliveredCount++; }
console.log(`Delivered orders: ${deliveredCount}`);
console.log(`Delivered revenue: BDT ${deliveredRevenue}`);
