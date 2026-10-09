function analyzeTemperatures(values) {
  if (!Array.isArray(values) || values.length === 0) return null;
  let min = values[0], max = values[0], sum = 0;
  for (const value of values) { if (value < min) min = value; if (value > max) max = value; sum += value; }
  return { min, max, average: sum / values.length };
}
console.log(JSON.stringify(analyzeTemperatures([28, 31, 30, 29, 32])));
