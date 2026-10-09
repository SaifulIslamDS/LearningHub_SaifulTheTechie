const hours = [2, 3, 0, 4, 5, 1];
let total = 0;
for (const h of hours) {
  if (h === 0) continue;
  total += h;
  if (total >= 10) break;
}
console.log(`Accumulated hours: ${total}`);
let countdown = 3;
while (countdown > 0) { console.log(`T-${countdown}`); countdown--; }
