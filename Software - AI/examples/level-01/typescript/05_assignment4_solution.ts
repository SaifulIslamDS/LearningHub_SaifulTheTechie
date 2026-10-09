type Student = { id: number; name: string; scores: number[] };

const average = (scores: number[]): number => scores.reduce((a,b)=>a+b,0) / scores.length;

function rankStudents(students: Student[]) {
  return students
    .map(student => ({ ...student, average: Number(average(student.scores).toFixed(1)) }))
    .sort((a,b) => b.average - a.average || a.name.localeCompare(b.name));
}

const ranked = rankStudents([
  { id: 1, name: "Asha", scores: [82, 91, 87] },
  { id: 2, name: "Rafi", scores: [90, 88, 84] },
  { id: 3, name: "Nila", scores: [95, 93, 96] }
]);
console.log(ranked.map(({name, average}) => `${name}: ${average}`).join("\n"));
