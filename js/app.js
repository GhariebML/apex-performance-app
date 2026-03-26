/* ══════════════════════════════════════════════════════════════════════════════
   APEX · App Core — Navigation, Sliders, Gender, Toast
   ══════════════════════════════════════════════════════════════════════════════ */

// ── Navigation ───────────────────────────────────────────────────────────────
function showPage(id, btn) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('page-' + id).classList.add('active');
  if (btn) btn.classList.add('active');
}

// ── Slider Values ────────────────────────────────────────────────────────────
function updateVal(id, val) {
  document.getElementById(id + '-val').textContent = val;
  updateSliderGradient(id);
}

function updateSliderGradient(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const min = +el.min, max = +el.max, val = +el.value;
  const pct = ((val - min) / (max - min)) * 100;
  el.style.background = `linear-gradient(90deg, var(--teal) ${pct}%, var(--border2) ${pct}%)`;
}

// ── Gender Toggle ────────────────────────────────────────────────────────────
let currentGender = 'M';
function setGender(g) {
  currentGender = g;
  document.getElementById('btn-M').classList.toggle('active', g === 'M');
  document.getElementById('btn-F').classList.toggle('active', g === 'F');
}

// ── Toast ────────────────────────────────────────────────────────────────────
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2500);
}

// ── Initialize ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Init all slider gradients
  document.querySelectorAll('input[type="range"]').forEach(el => {
    updateSliderGradient(el.id);
  });

  // Draw initial radar
  if (typeof drawRadar === 'function') {
    drawRadar({ bend: 20, situps: 35, jump: 160, grip: 35, fat: 20, systolic: 120 }, 'B');
  }

  // Animate hero stats on load
  animateHeroStats();
});

// ── Hero Stat Counter Animation ──────────────────────────────────────────────
function animateHeroStats() {
  document.querySelectorAll('.hero-stat .val').forEach(el => {
    const text = el.textContent;
    const match = text.match(/[\d,.]+/);
    if (!match) return;

    const target = parseFloat(match[0].replace(/,/g, ''));
    const hasComma = match[0].includes(',');
    const prefix = text.substring(0, text.indexOf(match[0]));
    const suffix = text.substring(text.indexOf(match[0]) + match[0].length);
    const isDecimal = match[0].includes('.');
    const duration = 1200;
    const start = performance.now();

    function tick(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      const current = target * eased;

      let display;
      if (isDecimal) {
        const decimals = match[0].split('.')[1]?.length || 1;
        display = current.toFixed(decimals);
      } else {
        display = Math.round(current).toString();
        if (hasComma) display = Number(display).toLocaleString();
      }
      el.textContent = prefix + display + suffix;

      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}
