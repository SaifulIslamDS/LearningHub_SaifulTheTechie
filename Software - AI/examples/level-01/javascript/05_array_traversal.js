const nums = [30, 5, 12, 100, 20];
const reversed = [...nums].reverse();
const sorted = [...nums].sort((a, b) => a - b);
console.log(`Original: ${nums.join(", ")}`);
console.log(`Reversed: ${reversed.join(", ")}`);
console.log(`Sorted: ${sorted.join(", ")}`);
