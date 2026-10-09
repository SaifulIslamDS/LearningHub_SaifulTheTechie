// REFERENCE-ONLY: requires mongodb and a running MongoDB deployment.
import { MongoClient, ObjectId } from "mongodb";
const client=new MongoClient(process.env.MONGODB_URI); await client.connect();
const collection=client.db("travel").collection("destinations");
await collection.insertOne({name:"Sundarbans",price:3200});
const rows=await collection.find({price:{$gte:2000}}).sort({price:-1}).limit(10).toArray();
await collection.updateOne({_id:new ObjectId(rows[0]._id)},{$set:{featured:true}});
console.log(rows); await client.close();
