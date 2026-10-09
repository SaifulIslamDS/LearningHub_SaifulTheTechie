type Course = {
  title: string;
  hours: number;
  published?: boolean;
};

function describeCourse(course: Course): string {
  const status = course.published ?? false;
  return `${course.title}: ${course.hours}h · published=${status}`;
}

const course: Course = { title: "TypeScript", hours: 16 };
console.log(describeCourse(course));
