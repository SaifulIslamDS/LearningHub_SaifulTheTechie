const expenses = [{category:"Food",amount:900},{category:"Transport",amount:450},{category:"Food",amount:350},{category:"Learning",amount:1200}];
const total = expenses.reduce((sum, item) => sum + item.amount, 0);
const byCategory = expenses.reduce((acc, item) => { acc[item.category] = (acc[item.category] ?? 0) + item.amount; return acc; }, {});
console.log(`Total: BDT ${total}`);
for (const [category, amount] of Object.entries(byCategory)) console.log(`${category}: ${amount}`);
