const filters={price:{$gte:2000,$lte:5000},tags:{$in:["featured","popular"]}};
const pipeline=[{$match:{status:"confirmed"}},{$group:{_id:"$destination",bookings:{$sum:1}}},{$sort:{bookings:-1}}];
console.log(JSON.stringify(filters)); console.log(JSON.stringify(pipeline));
