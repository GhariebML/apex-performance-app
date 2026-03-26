from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="APEX Body Performance API")

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
clf = None
reg = None
scaler = None
le_gender = None

def load_models():
    global clf, reg, scaler, le_gender
    try:
        clf = joblib.load("rf_classifier.joblib")
        reg = joblib.load("rf_regressor.joblib")
        scaler = joblib.load("scaler.joblib")
        le_gender = joblib.load("le_gender.joblib")
        print("Models loaded successfully.")
    except Exception as e:
        print(f"Warning: Could not load models. Run train.py first. Error: {e}")

load_models()

class PredictRequest(BaseModel):
    age: float
    gender: str
    height_cm: float
    weight_kg: float
    body_fat_pct: float
    diastolic: float
    systolic: float
    gripForce: float
    sit_and_bend_forward_cm: float
    sit_ups_counts: float
    broad_jump_cm: float

@app.post("/predict")
def predict_performance(req: PredictRequest):
    if clf is None or reg is None or scaler is None or le_gender is None:
        return {"error": "Models not loaded. Please run train.py to train models first."}
    
    # Prepare input data
    try:
        gender_encoded = le_gender.transform([req.gender.upper()])[0]
    except Exception:
        gender_encoded = 1 # Default to F or M depending on encoding
        
    input_data = pd.DataFrame([{
        'age': req.age,
        'gender': gender_encoded,
        'height_cm': req.height_cm,
        'weight_kg': req.weight_kg,
        'body fat_%': req.body_fat_pct,
        'diastolic': req.diastolic,
        'systolic': req.systolic,
        'gripForce': req.gripForce,
        'sit_and_bend_forward_cm': req.sit_and_bend_forward_cm,
        'sit-ups counts': req.sit_ups_counts,
        'broad jump_cm': req.broad_jump_cm
    }])
    
    # Scale input
    input_scaled = scaler.transform(input_data)
    
    # Predict Classification
    pred_class = clf.predict(input_scaled)[0]
    probs = clf.predict_proba(input_scaled)[0]
    class_probs = {c: float(p) for c, p in zip(clf.classes_, probs)}
    
    # Predict Regression (Broad Jump)
    # Regression model was trained on all features.
    pred_jump = reg.predict(input_scaled)[0]
    
    return {
        "predicted_class": pred_class,
        "probabilities": class_probs,
        "predicted_broad_jump_cm": round(float(pred_jump), 1),
        "model_version": "rf-v1.0"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
