function validateBooking(input) {
  const errors = [];
  if (!input.destinationId) errors.push("destinationId is required");
  if (!input.date) errors.push("date is required");
  if (!Number.isInteger(input.travellers) || input.travellers < 1) errors.push("travellers must be a positive integer");
  return errors;
}
function errorEnvelope(code, message, requestId) {
  return { error: { code, message, requestId } };
}
const valid = { destinationId: "dest_2", date: "2026-11-01", travellers: 2 };
const invalid = { destinationId: "", date: "", travellers: 0 };
console.log(`valid-errors=${validateBooking(valid).length}`);
console.log(JSON.stringify(errorEnvelope("VALIDATION_FAILED", validateBooking(invalid).join("; "), "req_demo_001")));
