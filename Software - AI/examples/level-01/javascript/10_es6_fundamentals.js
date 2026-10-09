const course = { title: "JavaScript", hours: 18, level: "Beginner" };
const { title, hours } = course;
const plan = { ...course, project: true };
const greet = (name = "Developer") => `Hello, ${name}!`;
console.log(greet("Saiful"));
console.log(`${title}: ${hours} hours`);
console.log(`Project included: ${plan.project}`);
console.log(course.missing?.value ?? "No optional value");
