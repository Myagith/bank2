// Theme colors to match CSS variables
const COLORS = {
  orange: getCssVar('--chart-orange') || '#ff8a00',
  orangeLight: getCssVar('--chart-orange-200') || '#ffd6a8',
  green: getCssVar('--chart-green') || '#6dd37a',
  blueDark: getCssVar('--chart-blue-900') || '#0f172a',
};

function getCssVar(name){
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

// Realistic sample data (could be replaced by API later)
const monthlyRevenue = [14, 22, 18, 26, 12, 33, 28, 24, 18, 20, 22, 25];
const monthlyOrders  = [8, 12, 9, 16, 7, 21, 18, 14, 11, 12, 13, 15];

const ctxBar = document.getElementById('barChart');
const barChart = new Chart(ctxBar, {
  type: 'bar',
  data: {
    labels: ['JAN','FEB','MAR','APR','MAY','JUNE','JULY','AUG','SEP','OCT','NOV','DEC'],
    datasets: [
      {
        label: 'Average rate',
        data: monthlyRevenue,
        backgroundColor: COLORS.orange,
        borderRadius: 8,
      },
      {
        label: 'Min rate',
        data: monthlyOrders,
        backgroundColor: COLORS.blueDark,
        borderRadius: 8,
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true }
    },
    scales: {
      x: { grid: { display: false } },
      y: { grid: { color: 'rgba(15,23,42,.08)' }, ticks: { stepSize: 10 } }
    }
  }
});

// Area chart
const ctxArea = document.getElementById('areaChart');
const areaChart = new Chart(ctxArea, {
  type: 'line',
  data: {
    labels: Array.from({length: 20}).map((_,i)=>`W${i+1}`),
    datasets:[{
      label: 'Daily rate',
      data: Array.from({length: 20}).map(()=> 20 + Math.round(Math.random()*20)),
      fill: true,
      borderColor: COLORS.green,
      backgroundColor: hexToRgba(COLORS.green, 0.25),
      tension: 0.35,
      pointRadius: 0
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display:false } },
    scales: { x: { display:false }, y: { grid: { color: 'rgba(15,23,42,.08)' } } }
  }
});

// Donut chart
const ctxDonut = document.getElementById('donutChart');
const donutChart = new Chart(ctxDonut, {
  type: 'doughnut',
  data: {
    labels: ['Up days', 'Down days', 'Flat'],
    datasets: [{
      data: [45, 35, 20],
      backgroundColor: [COLORS.green, COLORS.orange, COLORS.blueDark],
      hoverOffset: 6,
      cutout: '70%'
    }]
  },
  options: { plugins: { legend: { display: false } } }
});

// Simple calendar (current month)
(function renderCalendar(){
  const el = document.getElementById('calendar');
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const startWeekday = (firstDay.getDay() + 6) % 7; // Monday start
  const totalCells = startWeekday + lastDay.getDate();
  const weeks = Math.ceil(totalCells / 7);

  const header = document.createElement('div');
  header.style.display = 'flex';
  header.style.justifyContent = 'space-between';
  header.style.alignItems = 'center';
  header.style.marginBottom = '8px';
  const title = document.createElement('strong');
  title.textContent = now.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' });
  header.appendChild(title);
  el.appendChild(header);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = 'repeat(7, 1fr)';
  grid.style.gap = '4px';
  const weekdays = ['L','M','M','J','V','S','D'];
  weekdays.forEach(d => {
    const w = document.createElement('div');
    w.textContent = d;
    w.style.color = '#6b7280';
    w.style.fontSize = '12px';
    grid.appendChild(w);
  });

  // empty cells
  for(let i=0;i<startWeekday;i++) {
    const c = document.createElement('div');
    c.textContent = '';
    grid.appendChild(c);
  }

  // days
  for(let d=1; d<=lastDay.getDate(); d++){
    const cell = document.createElement('div');
    cell.textContent = String(d);
    cell.style.padding = '8px';
    cell.style.textAlign = 'center';
    cell.style.borderRadius = '8px';
    cell.style.cursor = 'pointer';
    cell.onmouseenter = () => cell.style.background = 'rgba(255,138,0,.1)';
    cell.onmouseleave = () => cell.style.background = '';

    if(d === now.getDate()){
      cell.style.background = hexToRgba(COLORS.orange, .15);
      cell.style.border = `1px solid ${hexToRgba(COLORS.orange, .35)}`;
      cell.style.fontWeight = '700';
    }

    grid.appendChild(cell);
  }

  el.appendChild(grid);
})();

function hexToRgba(hex, alpha){
  const h = hex.replace('#','');
  const bigint = parseInt(h, 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// =========================
// Fetch real data and update charts
// =========================
(async function loadRealData(){
  try {
    const today = new Date();
    const end = today.toISOString().slice(0,10);
    const startDate = new Date(today);
    startDate.setFullYear(today.getFullYear() - 1);
    const start = startDate.toISOString().slice(0,10);

    const url = `https://api.exchangerate.host/timeseries?base=USD&symbols=EUR&start_date=${start}&end_date=${end}`;
    const res = await fetch(url);
    const json = await res.json();
    if(!json || !json.rates) return;

    const entries = Object.entries(json.rates)
      .map(([date, obj]) => ({ date, value: obj.EUR }))
      .sort((a,b)=> a.date.localeCompare(b.date));

    // Area: last 30 days
    const last30 = entries.slice(-30);
    areaChart.data.labels = last30.map(e=> e.date.slice(5));
    areaChart.data.datasets[0].data = last30.map(e=> e.value);
    areaChart.update();

    // Bar: last 12 months average and min per month
    const monthKey = d => d.date.slice(0,7);
    const groups = {};
    for(const e of entries){
      const k = monthKey(e);
      (groups[k] ||= []).push(e.value);
    }
    const months = Object.keys(groups).sort().slice(-12);
    const avg = months.map(k=> groups[k].reduce((a,b)=>a+b,0)/groups[k].length);
    const min = months.map(k=> Math.min(...groups[k]));
    const monthLabels = months.map(k=> {
      const [y,m] = k.split('-').map(Number);
      const dt = new Date(y, m-1, 1);
      return dt.toLocaleString('en', { month: 'short' }).toUpperCase();
    });
    barChart.data.labels = monthLabels;
    barChart.data.datasets[0].data = avg;
    barChart.data.datasets[1].data = min;
    barChart.update();

    // Donut: up / down / flat days last 30 days
    let up=0, down=0, flat=0;
    for(let i=1;i<last30.length;i++){
      const diff = last30[i].value - last30[i-1].value;
      if(Math.abs(diff) < 1e-4) flat++; else if(diff > 0) up++; else down++;
    }
    donutChart.data.datasets[0].data = [up, down, flat];
    donutChart.update();
  } catch (e) {
    console.warn('Failed to load real data, using fallback.', e);
  }
})();