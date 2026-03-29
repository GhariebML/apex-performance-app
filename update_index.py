import sys

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

start_marker = '<div class="section-header" style="margin-top:28px;">\n    <h2>Feature Importance</h2>'
end_marker = '</section>\n\n<!-- ═══════════ PAGE: DATASET ═══════════ -->'

if start_marker in text and end_marker in text:
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    
    new_html = """<div class="section-header" style="margin-top:28px;">
    <h2>Classification Models</h2>
    <span class="sh-tag">DETAILED ANALYSIS</span>
    <div class="sh-line"></div>
  </div>

  <div class="model-dashboard-grid">
    <!-- RF -->
    <div class="model-card rf">
      <div class="model-card-head">
        <h3>Random Forest</h3>
        <span class="model-card-overview">Best overall robust bagging ensemble of 200 Decision Trees.</span>
      </div>
      <div class="model-metrics-grid">
        <div class="mm-item"><span class="mm-label">Accuracy</span><span class="mm-val" style="color:var(--teal)">75.1%</span></div>
        <div class="mm-item"><span class="mm-label">F1 Score</span><span class="mm-val" style="color:var(--teal)">75.0%</span></div>
      </div>
      <div class="model-pros-cons">
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Highest accuracy, robust to outliers and prevents overfitting.</span></div>
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Most stable across 80/20 & 50/50 splits.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Less interpretable than a single tree.</span></div>
      </div>
    </div>
    
    <!-- NN -->
    <div class="model-card nn">
      <div class="model-card-head">
        <h3>Neural Network</h3>
        <span class="model-card-overview">Multi-Layer Perceptron (128, 64) modeling highly non-linear boundaries.</span>
      </div>
      <div class="model-metrics-grid">
        <div class="mm-item"><span class="mm-label">Accuracy</span><span class="mm-val" style="color:var(--blue)">74.1%</span></div>
        <div class="mm-item"><span class="mm-label">F1 Score</span><span class="mm-val" style="color:var(--blue)">74.0%</span></div>
      </div>
      <div class="model-pros-cons">
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Top-tier accuracy predicting non-linear boundaries.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Sensitive to data volume; drops significantly on 50/50 split.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Least interpretable (black-box).</span></div>
      </div>
    </div>

    <!-- SVM -->
    <div class="model-card svm">
      <div class="model-card-head">
        <h3>Support Vector Machine</h3>
        <span class="model-card-overview">Hyperplane separation utilizing the RBF (Gaussian) Kernel.</span>
      </div>
      <div class="model-metrics-grid">
        <div class="mm-item"><span class="mm-label">Accuracy</span><span class="mm-val" style="color:var(--gold)">62.8%</span></div>
        <div class="mm-item"><span class="mm-label">F1 Score</span><span class="mm-val" style="color:var(--gold)">62.6%</span></div>
      </div>
      <div class="model-pros-cons">
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Very effective in high-dimensional feature spaces.</span></div>
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Strong non-linear capture with C=10.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Feature scaling is strictly mandatory for distance computations.</span></div>
      </div>
    </div>
    
    <!-- LR -->
    <div class="model-card lr">
      <div class="model-card-head">
        <h3>Logistic Regression</h3>
        <span class="model-card-overview">Linear multinomial classification optimized via L-BFGS.</span>
      </div>
      <div class="model-metrics-grid">
        <div class="mm-item"><span class="mm-label">Accuracy</span><span class="mm-val" style="color:#a061f0">57.2%</span></div>
        <div class="mm-item"><span class="mm-label">F1 Score</span><span class="mm-val" style="color:#a061f0">57.0%</span></div>
      </div>
      <div class="model-pros-cons">
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Highly interpretable feature coefficient analysis.</span></div>
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Outputs calibrated class probabilities well.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Struggles completely with non-linear class separations.</span></div>
      </div>
    </div>

    <!-- DT -->
    <div class="model-card dt">
      <div class="model-card-head">
        <h3>Decision Tree</h3>
        <span class="model-card-overview">Recursive partition splits maximizing node purity (Gini).</span>
      </div>
      <div class="model-metrics-grid">
        <div class="mm-item"><span class="mm-label">Accuracy</span><span class="mm-val" style="color:var(--green)">72.3%</span></div>
        <div class="mm-item"><span class="mm-label">Interpretability</span><span class="mm-val" style="color:var(--green)">Very High</span></div>
      </div>
      <div class="model-pros-cons">
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Fully interpretable branching and scaling not required.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Prone to high variance and overfitting deeper than max_depth=8.</span></div>
      </div>
    </div>
    
    <!-- KNN -->
    <div class="model-card knn">
      <div class="model-card-head">
        <h3>K-Nearest Neighbors</h3>
        <span class="model-card-overview">Instance-based learner computing Minkowski distances (k=11).</span>
      </div>
      <div class="model-metrics-grid">
        <div class="mm-item"><span class="mm-label">Accuracy</span><span class="mm-val" style="color:var(--red)">51.8%</span></div>
        <div class="mm-item"><span class="mm-label">F1 Score</span><span class="mm-val" style="color:var(--red)">51.6%</span></div>
      </div>
      <div class="model-pros-cons">
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Simple lazy learner with no training phase.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Lowest performer overall due to high dataset dimensionality.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Drops sharply on smaller data splits.</span></div>
      </div>
    </div>
  </div>

  <!-- Regression -->
  <div class="section-header" style="margin-top:28px;">
    <h2>Regression Models</h2>
    <span class="sh-tag">BROAD JUMP PREDICTION</span>
    <div class="sh-line"></div>
  </div>
  <div class="model-dashboard-grid">
    <div class="model-card rf">
      <div class="model-card-head">
        <h3>RF Regressor</h3>
        <span class="model-card-overview">Ensemble averaging across 200 jump-predicting trees.</span>
      </div>
      <div class="model-metrics-grid">
        <div class="mm-item"><span class="mm-label">R² Score</span><span class="mm-val" style="color:var(--teal)">~0.99</span></div>
        <div class="mm-item"><span class="mm-label">MAE</span><span class="mm-val" style="color:var(--white)">Near-Zero</span></div>
      </div>
      <div class="model-pros-cons">
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Best fit capturing complex agility metric interactions.</span></div>
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Extremely resilient to outliers.</span></div>
      </div>
    </div>
    
    <div class="model-card nn">
      <div class="model-card-head">
        <h3>Linear Regression</h3>
        <span class="model-card-overview">Standard multivariable linear approach.</span>
      </div>
      <div class="model-metrics-grid">
        <div class="mm-item"><span class="mm-label">R² Score</span><span class="mm-val" style="color:var(--blue)">~0.95</span></div>
        <div class="mm-item"><span class="mm-label">Fit</span><span class="mm-val" style="color:var(--blue)">Strong</span></div>
      </div>
      <div class="model-pros-cons">
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Confirms strong linear association between variables and jump.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Cannot fully capture peak performance explosive thresholds.</span></div>
      </div>
    </div>

    <div class="model-card svm">
      <div class="model-card-head">
        <h3>SVR (RBF Kernel)</h3>
        <span class="model-card-overview">Support Vector Regression utilizing insensitive tube (ε=0.1).</span>
      </div>
      <div class="model-metrics-grid">
        <div class="mm-item"><span class="mm-label">R² Score</span><span class="mm-val" style="color:var(--gold)">~0.91</span></div>
        <div class="mm-item"><span class="mm-label">Curve</span><span class="mm-val" style="color:var(--gold)">Non-Linear</span></div>
      </div>
      <div class="model-pros-cons">
        <div class="mpc-row"><span class="mpc-icon pro">✓</span><span class="mpc-text">Produces smooth continuous predictions unlike decision trees.</span></div>
        <div class="mpc-row"><span class="mpc-icon con">✕</span><span class="mpc-text">Highly sensitive to the hyperparameter C choices.</span></div>
      </div>
    </div>
  </div>
"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(text[:start_idx] + new_html + text[end_idx:])
    print("SUCCESS")
else:
    print("MARKERS NOT FOUND")
