const players = [
  { id: 1, name: "A", price: 40 },
  { id: 2, name: "B", price: 35 },
  { id: 3, name: "C", price: 55 }
];
const budget = 90;
const chosen = players.filter(p => p.price <= 40);
const cost = chosen.reduce((sum,p)=>sum+p.price,0);
console.log(`Chosen: ${chosen.map(p=>p.name).join(", ")}`);
console.log(`Cost: ${cost}, remaining: ${budget-cost}`);
