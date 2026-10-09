type Order = { id: number; total: number; status: "paid" | "pending" | "cancelled" };

function paidRevenue(orders: Order[]): number {
  return orders
    .filter(order => order.status === "paid")
    .reduce((sum, order) => sum + order.total, 0);
}

const orders: Order[] = [
  { id: 1, total: 1200, status: "paid" },
  { id: 2, total: 800, status: "pending" },
  { id: 3, total: 1700, status: "paid" }
];
console.log(`Paid revenue: BDT ${paidRevenue(orders)}`);
