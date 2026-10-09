const can=(role,action)=>({admin:["read","create","update","delete"],moderator:["read","update"],user:["read"]}[role]??[]).includes(action);
for(const role of ["admin","moderator","user"]){ console.log(`${role}: delete=${can(role,"delete")}`); }
