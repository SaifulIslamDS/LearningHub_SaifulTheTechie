---
title: MongoDB Queries, Operators & Aggregation
order: 1
summary: Move beyond basic CRUD with expressive query documents, update operators, projections, sorting, pagination and aggregation pipelines.
level: Intermediate
time: 95–130 min
curriculum_level: Level 01
source_module: '42'
source_type: source-curriculum
topics:
- Install and setup NoSQL Booster and know more about MongoDB methods
- 'Comparison Operators: $eq, $ne, $gt, $gte, $lt, $lte'
- 'Logical Operators: $and, $or, $not, $nor'
- 'Element & Type Operators: $exists, $type'
- 'Array Query Operators: $in, $nin, $all, $size, $elemMatch'
- 'Update Operators: $set, $inc, $push, $pull, $addToSet'
- 'Projection & Sorting: Include/Exclude using projection, sort(), limit(), skip()'
- 'Aggregation Pipeline: $match, $group, $project'
- 'Advanced Aggregation Operators: $lookup, $unwind,'
- Module Summary
prerequisites:
- level-01/l1-41-rest-api-and-crud-operations-with-express-and-mo/01-main
keywords:
- mongodb operators
- aggregation
- projection
- sort
- pagination
- lookup
- unwind
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
---
## Start here

CRUD answers *what operation* you want. Query operators answer *which documents* and *how data should be transformed*.

MongoDB queries are ordinary-looking JavaScript objects with special operator keys. That makes them approachable, but they still represent a database language. Learn to read them deliberately.

## What you will learn

- comparison and logical query operators;
- `$exists` and `$type`;
- array operators;
- update operators;
- projection, sorting, limit and skip;
- aggregation with `$match`, `$group` and `$project`;
- joining/reshaping with `$lookup` and `$unwind`;
- how a query-builder GUI such as NoSQLBooster can help exploration without replacing query understanding.

## 1. Build a query object first

The bundled `run/03_query_objects.mjs` creates this filter:

```js
const filters = {
  price: { $gte: 2000, $lte: 5000 },
  tags: { $in: ["featured", "popular"] },
};
```

<span class="output-label">Verified output</span>

```text
{"price":{"$gte":2000,"$lte":5000},"tags":{"$in":["featured","popular"]}}
```

Once you can read that object, passing it to `find(filters)` is straightforward.

## 2. Comparison operators

```js
{ price: { $eq: 3200 } }
{ price: { $ne: 3200 } }
{ price: { $gt: 3000 } }
{ price: { $gte: 3000 } }
{ price: { $lt: 5000 } }
{ price: { $lte: 5000 } }
```

Combine comparisons on one field to express a range.

## 3. Logical operators

```js
{
  $or: [
    { featured: true },
    { price: { $lt: 2000 } }
  ]
}
```

Use `$and`, `$or`, `$not` and `$nor` when the boolean structure cannot be expressed simply by multiple fields in one document.

## 4. Element and type checks

`$exists` asks whether a field is present. `$type` asks about its BSON type. These are useful when a flexible document schema has evolved over time and not every historical record has identical fields.

## 5. Arrays

```js
{ tags: { $in: ["featured"] } }
{ tags: { $all: ["featured", "family"] } }
{ tags: { $size: 2 } }
```

`$elemMatch` becomes important when a single array element must satisfy multiple conditions.

## 6. Update operators

Avoid reading a whole document, changing one field in JavaScript and replacing everything when the database can express the change directly:

```js
{ $set: { featured: true } }
{ $inc: { views: 1 } }
{ $push: { tags: "new" } }
{ $pull: { tags: "old" } }
{ $addToSet: { tags: "featured" } }
```

`$addToSet` is useful when you want set-like uniqueness in an array.

## 7. Projection and result windowing

```js
const rows = await collection
  .find({ featured: true })
  .project({ name: 1, price: 1 })
  .sort({ price: -1 })
  .skip(20)
  .limit(10)
  .toArray();
```

Projection reduces fields transferred. Sort defines stable order. Skip/limit provides simple pagination, though large-offset pagination has trade-offs you will learn later.

## 8. Aggregation is a pipeline

Think of documents flowing through stations:

```js
const pipeline = [
  { $match: { status: "confirmed" } },
  { $group: { _id: "$destination", bookings: { $sum: 1 } } },
  { $sort: { bookings: -1 } },
];
```

<span class="output-label">Verified pipeline object</span>

```text
[{"$match":{"status":"confirmed"}},{"$group":{"_id":"$destination","bookings":{"$sum":1}}},{"$sort":{"bookings":-1}}]
```

The release verified construction of this pipeline object. Execution against MongoDB is **REFERENCE-ONLY** because no server was connected.

## 9. `$lookup` and `$unwind`

`$lookup` can combine related data from another collection. `$unwind` expands array values into individual pipeline records. These tools are powerful, but repeated complex cross-collection relationships may also be a signal to think carefully about data modeling.

## Query-reading habit

For every complex query, translate it into plain English before running it. Example:

> Match confirmed bookings, group them by destination, count each group, then sort from most bookings to least.

If you cannot state the query in plain language, debugging it will be unnecessarily difficult.
