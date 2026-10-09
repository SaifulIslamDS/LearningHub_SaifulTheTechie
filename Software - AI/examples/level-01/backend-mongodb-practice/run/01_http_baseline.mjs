import http from "node:http";
const server=http.createServer((req,res)=>{res.setHeader("content-type","application/json");res.end(JSON.stringify({ok:true,path:req.url,method:req.method}));});
server.listen(0,"127.0.0.1",async()=>{const {port}=server.address();const data=await fetch(`http://127.0.0.1:${port}/api/health`).then(r=>r.json());console.log(`${data.method} ${data.path} -> ok=${data.ok}`);server.close();});
