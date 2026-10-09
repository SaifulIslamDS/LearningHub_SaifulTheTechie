const selected = ["Dhaka", "Khulna"];
const next = [...selected, "Chattogram"].filter((value, index, arr) => arr.indexOf(value) === index);
const removed = next.filter(city => city !== "Khulna");
console.log(next.join(", "));
console.log(removed.join(", "));
