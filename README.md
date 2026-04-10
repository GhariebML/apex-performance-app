<div align="center">

# 💪 APEX · Body Performance Intelligence
**AI-Powered Physical Fitness Classification & Athletic Prediction Platform**

<img src="banner.png" width="100%" alt="APEX Predictive Body Performance AI">

[![Live App](https://img.shields.io/badge/Deployed-Vercel-000000?style=for-the-badge&logo=vercel)](https://ghariebml.github.io/apex-performance-app)
[![Colab](https://img.shields.io/badge/Google%20Colab-Open%20Notebook-F9AB00?style=for-the-badge&logo=googlecolab)](https://drive.google.com/file/d/13jssUdICQhQ6--C2Y8-F38LCJAQjYp0z/view?usp=sharing)
[![Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=for-the-badge&logo=kaggle)](https://www.kaggle.com/datasets/kukuroo3/body-performance-data)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](/)

</div>

---

## 🚀 Overview

APEX is an advanced Machine Learning platform engineered to predict a subject's physical fitness performance class (Grades A–D) and estimate broad jump distance utilizing exactly **11 physiological measurements**. Trained on an extensive dataset of **13,393 real athletic evaluations**, this project represents a complete, production-grade end-to-end ML pipeline.

### The Pipeline Architecture
```text
Data Audit ➔ Deep EDA ➔ Outlier Capping (IQR) ➔ Split Training Strategy ➔ 5-Fold Cross Validation ➔ Live Deployment
```

---

## 🏆 Key Achievements

<div align="center">

| Metric | Recorded Value | Winning Algorithm |
| :--- | :--- | :--- |
| **Peak Accuracy** | **74.26%** | Random Forest Classifier (70/30) |
| **Best CV Stability** | **74.00% ± 1.12%**| Neural Network (MLP) (5-Fold) |
| **Regression Performance** | **0.7842 R²** | RF Regressor (Broad Jump) |
| **Leading Indicator** | `0.258 Importance`| Sit & Bend Forward (cm) |

</div>

---

## 📊 Comprehensive Model Benchmarks

### 🎯 Classification Matrix (70/30 Split)

| Algorithm | Validation Accuracy | Precision | Recall | Stability (80/20 ➔ 50/50) |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | **74.26%** | 74.71% | 74.26% | Excellent (Δ1.9%) |
| Neural Network (MLP) | 74.06% | 75.19% | 74.06% | Excellent |
| SVM (RBF Kernel) | 71.62% | 72.12% | 71.62% | Strong (Δ1.1%) |
| Decision Tree | 65.17% | 66.79% | 65.17% | Moderate |
| Logistic Regression | 62.36% | 62.05% | 62.36% | Moderate |
| KNN (k=11) | 61.84% | 63.81% | 61.84% | Volatile |

### 🏋️ Feature Significance Discovery
Through Permutation Importance evaluating the Random Forest Model, we disrupted standard physiological assumptions:

> **Key Finding:** Flexibility (`sit_and_bend_forward_cm` - 0.258) and core endurance (`sit-ups` - 0.231) combined account for **48.9%** of the model's total predictive power. This decisively proved that functional biomechanics drastically outweigh static body composition (`body_fat_%` - 0.058) metrics in determining elite athletic grades.

---

## ⚙️ Running APEX Locally

### Option 1: Live Cloud Exploration (Recommended)
You can directly run our entire ML pipeline and view the EDA visualizations without installing anything:
[![Colab Launch](https://img.shields.io/badge/Launch%20in%20Google%20Colab-Launch-000?style=for-the-badge&logo=googlecolab)](https://drive.google.com/file/d/13jssUdICQhQ6--C2Y8-F38LCJAQjYp0z/view?usp=sharing)

### Option 2: Full Local Environment
To explore the codebase and launch the live interactive dashboard:

```bash
# Clone repository
git clone https://github.com/GhariebML/apex-performance-app.git
cd apex-performance-app

# Install ML Dependencies
pip install -r requirements.txt fastapi uvicorn scikit-learn joblib

# Serve the Backend RestAPI
uvicorn main:app --reload

# Serve the Frontend HTML/JS (In a new terminal)
npx live-server .
```

---

## 🏗️ Technical File Structure

```text
apex-performance-app/
├── index.html                              # High-Performance Vanilla JS Frontend
├── css/                                    # Responsive Tokens & UI Styles
├── js/
│   ├── predict.js                          # Local-fallback JavaScript Prediction Engine
│   ├── ui.js                               # DOM Rendering & Insights Graphing
│   ├── radar.js                            # HTML5 Canvas Performance Radar Visualization
│   └── history.js                          # State Management & Comparison Modules
├── 03_Snipers_Team_ML_Notebook_Final.ipynb # Core AI Pipeline
├── Analytics_Notebook.ipynb                # Extensive EDA & Statistical Notebook
├── bodyPerformance.csv                     # Raw Baseline Database
└── *.joblib                                # Serialized Inference Models (RF, Scaler, Encoders)
```

---

## 🤝 The Development Team

Developed as a flagship machine learning Capstone project for the **Military Technical College (2026)**.

| Engineer | Specialization |
| :--- | :--- |
| **Mohamed Gharieb** | *Team Leader & Deep Learning Architect (MLP)* |
| **Saad** | *Data Engineering & Distance Algorithms (KNN)* |
| **El Kholy** | *Statistical Modeling & Logistic Regression* |
| **Wael** | *Visualization Lead & Ensemble Tree Modeling* |
| **Hesham** | *Support Vector Architecture (Linear/RBF)* |

---
<div align="center">
  <sub>Built with 🧠 and ☕ by the Gharieb Team - 2026</sub>
</div>
