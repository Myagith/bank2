/* Dashboard charts: line, bar and gauge-like doughnut */

function asCurrency(v){
  try { return new Intl.NumberFormat(undefined, {style:'currency', currency:'USD'}).format(v); } catch(e){ return v; }
}

export async function renderAdminCharts(){
  const txResp = await fetch('/dashboard/api/transactions/monthly/');
  const tx = await txResp.json();
  const ctxLine = document.getElementById('txChart');
  if(ctxLine){
    new Chart(ctxLine, { type:'line', data:{ labels:tx.labels, datasets:[{ label:'Volumes', data:tx.values, borderColor:'#ff8800', backgroundColor:'rgba(255,136,0,0.15)', tension:.35, fill:true }]}, options:{ plugins:{legend:{display:true}}, responsive:true, scales:{ y:{ beginAtZero:true } } });
  }

  const byTypeResp = await fetch('/dashboard/api/transactions/monthly-by-type/');
  const byType = await byTypeResp.json();
  const ctxBar = document.getElementById('typeChart');
  if(ctxBar){
    new Chart(ctxBar, { type:'bar', data:{ labels:byType.labels, datasets:[ {label:'Dépôts', data:byType.deposit, backgroundColor:'rgba(0,184,148,.7)'}, {label:'Retraits', data:byType.withdraw, backgroundColor:'rgba(255,99,132,.7)'} ] }, options:{ responsive:true, scales:{ y:{ beginAtZero:true } } });
  }

  const total = (tx.values||[]).reduce((a,b)=>a+b,0);
  const target = Math.max(1000, total*1.2);
  const gauge = document.getElementById('gauge');
  if(gauge){
    new Chart(gauge, { type:'doughnut', data:{ labels:['Atteint','Reste'], datasets:[{ data:[total, Math.max(0,target-total)], backgroundColor:['#ff8800','#e9ecef'] }] }, options:{ cutout:'70%', plugins:{legend:{display:false}, tooltip:{callbacks:{label:(c)=>asCurrency(c.parsed)}}} });
    const center = gauge.parentElement.querySelector('.gauge-center');
    if(center){ center.textContent = asCurrency(total); }
  }
}

export async function renderClientCharts(){
  const txResp = await fetch('/dashboard/api/transactions/monthly/');
  const tx = await txResp.json();
  const ctx = document.getElementById('clientBar');
  if(ctx){
    new Chart(ctx, { type:'bar', data:{ labels:tx.labels, datasets:[{label:'Mes montants', data:tx.values, backgroundColor:'rgba(0,150,136,.6)'}]}, options:{responsive:true, scales:{y:{beginAtZero:true}}} });
  }
}

