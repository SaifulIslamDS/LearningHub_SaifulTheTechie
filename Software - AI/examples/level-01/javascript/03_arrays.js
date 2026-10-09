const skills = ["HTML", "CSS", "JavaScript"];
skills.push("Git");
skills.unshift("Problem Solving");
const removed = skills.pop();
console.log(`Count: ${skills.length}`);
console.log(`First: ${skills[0]}`);
console.log(`Removed: ${removed}`);
console.log(skills.join(" | "));
