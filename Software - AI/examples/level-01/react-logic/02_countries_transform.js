const countries = [
  { name: "Bangladesh", population: 173562364, region: "Asia" },
  { name: "Japan", population: 123753041, region: "Asia" },
  { name: "Canada", population: 39742430, region: "Americas" }
];
const asia = countries.filter(c => c.region === "Asia").map(c => c.name);
console.log(`Asian countries: ${asia.join(", ")}`);
