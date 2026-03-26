/* ══════════════════════════════════════════════════════════════════════════════
   APEX · UI Controller — runPredict + DOM Updates
   ══════════════════════════════════════════════════════════════════════════════ */

async function runPredict() {
  const btn = document.querySelector('.predict-btn');
  btn.innerHTML = '<span class="spinner"></span> ANALYZING...';
  btn.disabled = true;

  try {
    const inputs = {
      age:       +document.getElementById('age').value,
      gender:    currentGender,
      height_cm: +document.getElementById('height').value,
      weight_kg: +document.getElementById('weight').value,
      body_fat_pct: +document.getElementById('fat').value,
      diastolic: +document.getElementById('diastolic').value,
      systolic:  +document.getElementById('systolic').value,
      gripForce: +document.getElementById('grip').value,
      sit_and_bend_forward_cm: +document.getElementById('bend').value,
      sit_ups_counts: +document.getElementById('situps').value,
      broad_jump_cm: +document.getElementById('jump').value,
    };

    // Validate BP
    if (inputs.systolic <= inputs.diastolic) {
      showToast('⚠ Systolic must exceed diastolic BP');
      btn.innerHTML = '⚡ ANALYZE PERFORMANCE';
      btn.disabled = false;
      return;
    }

    // Phase 1 API integration
    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(inputs)
    });
    
    if (!response.ok) throw new Error('Network response was not ok');
    const data = await response.json();

    if (data.error) throw new Error(data.error);

    const cls = data.predicted_class;
    const probs = data.probabilities;
    const jumpEst = data.predicted_broad_jump_cm;

    // --- Update class card ---
    const card = document.getElementById('class-result-card');
    card.className = 'class-result-card class-' + cls;
    document.getElementById('placeholder-state').style.display = 'none';
    const body = document.getElementById('class-result-body');
    body.style.display = 'block';

    const badge = document.getElementById('class-badge');
    badge.className = 'class-badge-big ' + cls;
    badge.textContent = cls;

    document.getElementById('class-name').textContent = CLASS_INFO[cls].name;
    document.getElementById('class-desc').textContent = CLASS_INFO[cls].desc;

    // Prob bars
    ['A', 'B', 'C', 'D'].forEach(c => {
      const pct = Math.round(probs[c] * 100);
      document.getElementById('prob-' + c).style.width = pct + '%';
      document.getElementById('pct-' + c).textContent = pct + '%';
    });

    // Jump
    document.getElementById('jump-pred').innerHTML = jumpEst + ' <span class="unit">cm</span>';
    document.getElementById('jump-bench').textContent = JUMP_BENCHMARKS[cls];

    // Radar mapping for chart (requires original names)
    const radarInputs = {
      bend: inputs.sit_and_bend_forward_cm,
      situps: inputs.sit_ups_counts,
      jump: inputs.broad_jump_cm,
      grip: inputs.gripForce,
      fat: inputs.body_fat_pct,
      systolic: inputs.systolic
    };
    drawRadar(radarInputs, cls);

    // Tips
    const tips = CLASS_TIPS[cls];
    document.getElementById('tips-list').innerHTML = tips.map(t =>
      `<div class="tip-item"><span class="tip-icon">${t.icon}</span><span>${t.text}</span></div>`
    ).join('');

    btn.innerHTML = '✓ ANALYSIS COMPLETE';
    btn.style.background = 'linear-gradient(135deg, var(--green), #009948)';
    showToast('✓ Performance Class ' + cls + ' · ' + jumpEst + ' cm jump');

    setTimeout(() => {
      btn.innerHTML = '⚡ ANALYZE PERFORMANCE';
      btn.style.background = '';
      btn.disabled = false;
    }, 2400);

  } catch (err) {
    showToast('⚠ API Error: ' + err.message);
    btn.innerHTML = '⚡ ANALYZE PERFORMANCE';
    btn.disabled = false;
  }
}
