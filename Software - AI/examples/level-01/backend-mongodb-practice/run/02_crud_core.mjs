const destinations=[];
const create = name => { const item={id:String(destinations.length+1),name}; destinations.push(item); return item; };
const update = (id,name) => { const item=destinations.find(x=>x.id===id); if(item)item.name=name; return item; };
const remove = id => { const i=destinations.findIndex(x=>x.id===id); return i>=0?destinations.splice(i,1)[0]:null; };
create("Cox's Bazar"); create("Sundarbans"); update("2","Sundarbans Mangrove"); remove("1");
console.log(JSON.stringify(destinations));
