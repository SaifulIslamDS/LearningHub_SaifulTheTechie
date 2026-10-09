// REFERENCE-ONLY: requires the express package.
import express from "express";
const app=express(); app.use(express.json());
app.get("/api/destinations", async (req,res)=>res.json({data:[]}));
app.post("/api/destinations", async (req,res)=>res.status(201).json({data:req.body}));
app.listen(4000);
