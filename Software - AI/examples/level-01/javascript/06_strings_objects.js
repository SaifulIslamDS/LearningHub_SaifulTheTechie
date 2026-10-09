const raw = "  Saiful The Techie  ";
const clean = raw.trim().toLowerCase();
const profile = { name: "Saiful Islam", skills: ["JavaScript", "Git"], contact: { city: "Dhaka" } };
profile.skills.push("React");
console.log(clean);
console.log(profile.name);
console.log(profile.contact.city);
console.log(profile.skills.join(", "));
