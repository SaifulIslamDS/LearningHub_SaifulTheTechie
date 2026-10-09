const products = [{name:"Keyboard",price:2500,stock:5},{name:"Mouse",price:900,stock:0},{name:"Monitor",price:18000,stock:3}];
const available = products.filter(p => p.stock > 0);
const labels = available.map(p => `${p.name}: BDT ${p.price}`);
console.log(labels.join("\n"));
