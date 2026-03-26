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

    // Age & Gender Adjusted Benchmark
    let baseJump = 260 - (inputs.age - 20) * 1.5;
    if (inputs.gender === 'F') baseJump -= 45;
    const benchMsg = `Age/Gender Benchmark (A-tier): ~${Math.max(100, Math.round(baseJump))} cm`;
    
    document.getElementById('jump-pred').innerHTML = jumpEst + ' <span class="unit">cm</span>';
    document.getElementById('jump-bench').textContent = benchMsg;

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

    // Intelligent Tips Engine based on weakest features
    const normalize = v => Math.max(0, Math.min(1, v));
    const featureScores = [
      { name: 'Flexibility', val: normalize((inputs.sit_and_bend_forward_cm + 25) / 225), tip: 'Add daily flexibility work to improve sit-and-bend distance.' },
      { name: 'Core', val: normalize(inputs.sit_ups_counts / 80), tip: 'Increase sit-up volume by 15% to strengthen core.' },
      { name: 'Explosive Power', val: normalize((inputs.broad_jump_cm - 50) / 250), tip: 'Incorporate explosive plyometric exercises.' },
      { name: 'Grip Strength', val: normalize(inputs.gripForce / 70), tip: 'Prioritize grip strength training (farmer walks, hangs).' },
      { name: 'Body Composition', val: normalize(1 - (inputs.body_fat_pct - 3) / 62), tip: 'Reduce body fat through nutrition and cardio conditioning.' },
      { name: 'Cardio Efficiency', val: normalize(1 - Math.abs((inputs.systolic - 115) / 85)), tip: 'Improve blood pressure via steady-state endurance training.' }
    ];
    
    featureScores.sort((a,b) => a.val - b.val);
    const dynamicTips = [
      { icon: '🎯', text: `Focus area (${featureScores[0].name.toUpperCase()}): ${featureScores[0].tip}` },
      { icon: '📈', text: `Secondary target (${featureScores[1].name.toUpperCase()}): ${featureScores[1].tip}` },
      { icon: '💡', text: typeof CLASS_TIPS !== 'undefined' ? CLASS_TIPS[cls][0].text : 'Keep pushing forward to reach the next tier.' }
    ];

    document.getElementById('tips-list').innerHTML = dynamicTips.map(t =>
      `<div class="tip-item"><span class="tip-icon">${t.icon}</span><span>${t.text}</span></div>`
    ).join('');

    // Save to History (LocalStorage)
    if(typeof saveToHistory === 'function') {
      saveToHistory(inputs, cls, probs, jumpEst);
    }

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
