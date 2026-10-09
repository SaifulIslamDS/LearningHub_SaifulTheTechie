
(function(){
 const input=document.querySelector('#site-search'),out=document.querySelector('#search-results');if(!input||!out)return;
 const cur=(window.ST_CURRICULUM||[]).map(x=>({title:x.title,topics:x.topics||[],meta:`Level 0${x.level} · ${x.milestone} · Module ${x.number}`,url:`${x.level===1?'level-01':'level-02'}/modules/${x.id}.html`,status:x.status,type:'Curriculum'}));
 const extra=(window.ST_EXTRA_SEARCH||[]);const data=[...cur,...extra];
 const esc=s=>String(s).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
 function draw(){const q=input.value.trim().toLowerCase();if(!q){out.innerHTML='<div class="callout">Try <strong>semantic HTML</strong>, <strong>Flexbox</strong>, <strong>Git</strong>, <strong>accessibility</strong>, <strong>portfolio</strong> or <strong>debugging</strong>.</div>';return}const hits=data.filter(x=>(x.title+' '+(x.topics||[]).join(' ')+' '+(x.meta||'')+' '+(x.type||'')).toLowerCase().includes(q)).slice(0,60);out.innerHTML=hits.length?hits.map(x=>`<article class="result"><span class="tag ${x.type==='Curriculum'?'source':'ready'}">${esc(x.type||'Learning')}</span><h3><a href="${x.url}">${esc(x.title)}</a></h3><small>${esc(x.meta||'')}</small><p>${esc((x.topics||[]).slice(0,5).join(' · '))}</p></article>`).join(''):'<div class="callout warn">No result matched that search.</div>'}
 input.addEventListener('input',draw);draw();
})();
