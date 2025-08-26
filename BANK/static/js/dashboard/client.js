document.addEventListener('DOMContentLoaded', () => {
  const dataEl = document.getElementById('client-dashboard-data');
  if (!dataEl) return;
  const payload = JSON.parse(dataEl.textContent || '{}');

  const totalExpenses = payload.total_expenses || 0;
  const totalDeposits = payload.total_deposits || 0;
  const lastDaysLabels = payload.last_days_labels || [];
  const lastDaysExpenses = payload.last_days_expenses || [];

  const pieCtx = document.getElementById('expensesDepositsPie');
  if (pieCtx) {
    new Chart(pieCtx, {
      type: 'pie',
      data: {
        labels: ['Dépenses', 'Dépôts'],
        datasets: [{
          data: [totalExpenses, totalDeposits],
          backgroundColor: ['#ff8800', '#32cd32']
        }]
      },
      options: { responsive: true }
    });
  }

  const lineCtx = document.getElementById('expensesChart');
  if (lineCtx) {
    new Chart(lineCtx, {
      type: 'line',
      data: {
        labels: lastDaysLabels,
        datasets: [{
          label: 'Dépenses',
          data: lastDaysExpenses,
          borderColor: '#ff8800',
          backgroundColor: 'rgba(255,136,0,0.2)',
          fill: true,
          tension: 0.35
        }]
      },
      options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
  }
});