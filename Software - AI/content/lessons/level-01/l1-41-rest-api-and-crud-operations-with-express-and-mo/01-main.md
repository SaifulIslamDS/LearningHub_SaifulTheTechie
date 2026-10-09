---
title: REST CRUD with Express & MongoDB
order: 1
summary: Connect a REST API to MongoDB and implement create, read, update and delete operations with clear HTTP contracts.
level: Intermediate
time: 100–140 min
curriculum_level: Level 01
source_module: '41'
source_type: source-curriculum
topics:
- 'Database Setup: Creating a MongoDB Atlas Account'
- 'Connection Logic: Async/Await & Try-Catch Block'
- 'Create Operation: Create client-side and set POST operation'
- Recap POST method and know about insertOne
- Display user Data in Client side UI
- Delete user from UI and Database & explore ObjectId
- 'Read Operation: Loading Single Item by ID'
- 'Update Operation: PUT vs PATCH & Updating Data'
- Update data and display on UI
- (Optional) Running MongoDB Locally (No Internet)
prerequisites:
- level-01/l1-40-node-js-and-express-from-setup-to-first-api/01-main
keywords:
- mongodb
- crud
- objectid
- put
- patch
- atlas
- rest api
reviewed: '2026-10-09'
files:
- level-01/backend-mongodb-practice.zip
resources:
- title: MongoDB Node.js Driver
  url: https://www.mongodb.com/docs/drivers/node/current/
  source: MongoDB
  note: Official Node.js driver documentation.
- title: Find documents
  url: https://www.mongodb.com/docs/drivers/node/current/crud/query/retrieve/
  source: MongoDB
  note: Official query and find operation guidance.
- title: Aggregation operations
  url: https://www.mongodb.com/docs/drivers/node/current/aggregation/
  source: MongoDB
  note: Official aggregation pipeline guide.
youtube:
  title: CRUD API Tutorial — Node, Express, MongoDB
  creator: freeCodeCamp.org
  url: https://www.youtube.com/watch?v=_7UQPve99r4
  video_id: _7UQPve99r4
  duration: ≈1 h 30 min
  language: English
  level: Beginner / Intermediate
  reviewed: '2026-10-09'
  why_recommended: A build-oriented CRUD API course that visually reinforces Express setup, MongoDB, create/read/update/delete routes, controllers and API testing. Watch the matching sections rather than treating the video as a replacement for this tutorial.
  timestamps:
  - label: MongoDB setup
    time: '20:40'
  - label: Create API
    time: '41:19'
  - label: Read / update / delete
    time: '48:19'
  - label: Routes and controllers
    time: '1:12:19'
---
## Start here

CRUD is easy to memorize and easy to implement badly. The real skill is keeping the HTTP contract, database operation and UI state consistent.

```text
HTTP intent       MongoDB operation
POST create   →   insertOne
GET read      →   find / findOne
PATCH update  →   updateOne
DELETE delete →   deleteOne
```

The bundled practice package first proves CRUD behavior with an in-memory script, then provides a MongoDB reference file for the same ideas.

## What you will learn

- create an Atlas/local connection configuration;
- handle async connection failures;
- create a record with `insertOne`;
- list and load one document;
- work with MongoDB `ObjectId`;
- delete a record;
- understand PUT vs PATCH;
- update a record and reflect it in UI;
- run MongoDB locally as an optional alternative.

## 1. Verify the CRUD lifecycle without a database

Run `run/02_crud_core.mjs`. It creates two destinations, updates one and deletes one.

<span class="output-label">Verified output</span>

```text
[{"id":"2","name":"Sundarbans Mangrove"}]
```

This isolates the **application lifecycle** from the database driver. If this logic makes sense, MongoDB becomes a persistence implementation rather than magic.

## 2. Connect once, reuse the client

Reference shape:

```js
import { MongoClient } from "mongodb";

const client = new MongoClient(process.env.MONGODB_URI);
await client.connect();

const db = client.db("travel");
const destinations = db.collection("destinations");
```

Keep the URI in an environment variable. Catch connection errors at startup and fail clearly rather than letting every request discover the problem independently.

## 3. Create

```js
const result = await destinations.insertOne({
  name: "Sundarbans",
  price: 3200,
  featured: false,
});
```

Your API should validate the payload before insertion. A successful create endpoint commonly returns status `201` plus either the new representation or its identifier.

## 4. Read the collection

```js
const rows = await destinations
  .find({})
  .sort({ name: 1 })
  .toArray();
```

A cursor represents a potentially large result. Do not assume every production collection should be converted into one huge array; pagination comes later.

## 5. Load a document by `_id`

MongoDB's default IDs are BSON `ObjectId` values, not ordinary arbitrary strings. Convert a route parameter before querying:

```js
import { ObjectId } from "mongodb";

const id = new ObjectId(req.params.id);
const item = await destinations.findOne({ _id: id });
```

Validate invalid IDs and return an appropriate client response rather than allowing a constructor error to leak as an opaque 500.

## 6. Delete

```js
const result = await destinations.deleteOne({ _id: id });
```

Check `deletedCount`. A request can be syntactically correct while matching no document.

## 7. PUT vs PATCH

Use the distinction to communicate the contract:

- **PUT** traditionally represents replacing the resource representation;
- **PATCH** represents partial changes.

A partial update in this project fits `PATCH`:

```js
await destinations.updateOne(
  { _id: id },
  { $set: { name, price } }
);
```

## 8. Frontend update flow

```text
edit form
   ↓ PATCH /api/destinations/:id
server validates + updates MongoDB
   ↓
response contains updated state
   ↓
frontend updates list/detail UI
```

Do not update the UI optimistically and forget what happens when the server rejects the request.

## 9. Atlas vs local MongoDB

Atlas provides managed MongoDB. A local community deployment can be useful offline or for learning. The API code should depend on `MONGODB_URI`, not hard-code one environment, so you can switch without rewriting your routes.

## Practice package

`reference/mongo-crud.mjs` contains the MongoDB driver version. It is **REFERENCE-ONLY** because no MongoDB deployment was available in this release environment. The in-memory CRUD script above was executed and its output is real.
