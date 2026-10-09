function total(values) { let sum = 0; for (const value of values) sum += value; return sum; }
function evenOnly(values) { return values.filter(n => n % 2 === 0); }
console.log(`Total: ${total([120, 80, 200])}`);
console.log(`Even: ${evenOnly([3, 4, 7, 10, 12]).join(", ")}`);
