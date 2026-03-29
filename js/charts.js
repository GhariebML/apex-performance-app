/* ══════════════════════════════════════════════════════════════════════════════
   APEX · Charts — 3-Split Comparison & K-Fold CV Results
   ══════════════════════════════════════════════════════════════════════════════ */

// ── Real data from notebook outputs ──────────────────────────────────────────
const SPLIT_DATA = {
  labels: ['Random Forest', 'Neural Network', 'SVM (RBF)', 'Decision Tree', 'Logistic Reg', 'KNN'],
  '80/20': [74.01, 72.40, 71.14, 63.78, 63.14, 62.55],
  '70/30': [74.26, 74.06, 71.62, 65.17, 62.36, 61.84],
  '50/50': [72.36, 72.38, 70.51, 64.43, 62.32, 61.71],
};

const CV_RESULTS = [
  { model: 'Random Forest',    mean: 73.32, std: 0.78,  color: 'var(--teal)',  bar: 99 },
  { model: 'Neural Network',   mean: 74.00, std: 1.12,  color: 'var(--blue)',  bar: 100 },
  { model: 'SVM (RBF)',        mean: 70.90, std: 0.69,  color: 'var(--gold)',  bar: 96 },
  { model: 'Decision Tree',    mean: 64.75, std: 0.80,  color: 'var(--green)', bar: 87 },
  { model: 'Logistic Reg',     mean: 61.67, std: 0.83,  color: '#a061f0',      bar: 83 },
  { model: 'KNN',              mean: 62.08, std: 0.72,  color: 'var(--red)',   bar: 84 },
];

// ── Stability deltas (best 80/20 - worst split) ───────────────────────────────
const STABILITY = [
  { model: 'SVM (RBF)',        delta: 1.11, rating: '⚡ Most Stable',  color: 'var(--teal)' },
  { model: 'Random Forest',    delta: 1.90, rating: '✅ Very Stable',   color: 'var(--teal)' },
  { model: 'KNN',              delta: 0.84, rating: '⚠️ Low Variance',  color: 'var(--gold)' },
  { model: 'Neural Network',   delta: 1.68, rating: '✅ Very Stable',   color: 'var(--teal)' },
  { model: 'Decision Tree',    delta: 1.39, rating: '✅ Stable',        color: 'var(--blue)' },
  { model: 'Logistic Reg',     delta: 0.82, rating: '⚠️ Low Variance',  color: 'var(--gold)' },
];

// ── Draw the split comparison chart ──────────────────────────────────────────
let splitChart = null;

function initSplitChart() {
  const canvas = document.getElementById('split-chart');
  if (!canvas || typeof Chart === 'undefined') return;

  const ctx = canvas.getContext('2d');

  const gridColor = 'rgba(255,255,255,0.06)';
  const tickColor = 'rgba(255,255,255,0.4)';

  splitChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: SPLIT_DATA.labels,
      datasets: [
        {
          label: '80/20 Split',
          data: SPLIT_DATA['80/20'],
          backgroundColor: 'rgba(0,229,200,0.65)',
          borderColor: 'rgba(0,229,200,0.9)',
          borderWidth: 1,
          borderRadius: 3,
          borderSkipped: false,
        },
        {
          label: '70/30 Split',
          data: SPLIT_DATA['70/30'],
          backgroundColor: 'rgba(77,159,255,0.65)',
          borderColor: 'rgba(77,159,255,0.9)',
          borderWidth: 1,
          borderRadius: 3,
          borderSkipped: false,
        },
        {
          label: '50/50 Split',
          data: SPLIT_DATA['50/50'],
          backgroundColor: 'rgba(240,165,0,0.65)',
          borderColor: 'rgba(240,165,0,0.9)',
          borderWidth: 1,
          borderRadius: 3,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 1000, easing: 'easeInOutQuart' },
      plugins: {
        legend: {
          position: 'top',
          align: 'end',
          labels: {
            color: tickColor,
            font: { family: "'Space Mono', monospace", size: 11 },
            boxWidth: 12,
            boxHeight: 12,
            padding: 16,
          },
        },
        tooltip: {
          backgroundColor: 'rgba(8,12,24,0.95)',
          borderColor: 'rgba(0,229,200,0.3)',
          borderWidth: 1,
          titleColor: 'rgba(255,255,255,0.9)',
          bodyColor: 'rgba(255,255,255,0.6)',
          padding: 12,
          callbacks: {
            label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y.toFixed(2)}%`,
          },
        },
      },
      scales: {
        x: {
          grid: { color: gridColor },
          ticks: {
            color: tickColor,
            font: { family: "'Space Mono', monospace", size: 10 },
            maxRotation: 15,
            minRotation: 0,
          },
        },
        y: {
          min: 55,
          max: 80,
          grid: { color: gridColor },
          ticks: {
            color: tickColor,
            font: { family: "'Space Mono', monospace", size: 10 },
            callback: v => v + '%',
            stepSize: 5,
          },
        },
      },
      interaction: { mode: 'index', intersect: false },
    },
  });
}

// ── Render CV Results table rows ──────────────────────────────────────────────
function renderCVResults() {
  const tbody = document.getElementById('cv-tbody');
  if (!tbody) return;

  tbody.innerHTML = CV_RESULTS.map((r, i) => `
    <tr class="cv-row">
      <td class="cv-rank">${['🥇','🥈','🥉','4','5','6'][i]}</td>
      <td class="cv-model" style="color:${r.color}">${r.model}</td>
      <td class="cv-mean">${r.mean.toFixed(2)}%</td>
      <td class="cv-std">±${r.std.toFixed(2)}%</td>
      <td class="cv-bar-cell">
        <div class="cv-bar-track">
          <div class="cv-bar-fill" style="width:${r.bar}%; background:${r.color};"></div>
        </div>
      </td>
    </tr>
  `).join('');
}

// ── Init on DOM ready ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  renderCVResults();
  // Defer chart slightly so Chart.js CDN has fully parsed
  setTimeout(initSplitChart, 100);
});
