import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

def load_and_preprocess_data(filepath="bodyPerformance.csv"):
    if not os.path.exists(filepath):
        print(f"Error: Dataset {filepath} not found.")
        return None, None, None, None, None, None
        
    print(f"Loading dataset from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Clean data (drop duplicates, handle logic)
    df = df.drop_duplicates()
    
    # Encode categorical
    le_gender = LabelEncoder()
    df['gender'] = le_gender.fit_transform(df['gender'])
    
    # Split features and target
    X = df.drop(columns=['class'])
    y_class = df['class']
    y_reg = df['broad jump_cm']
    
    # Train test split for classification
    X_train, X_test, y_c_train, y_c_test = train_test_split(X, y_class, test_size=0.3, random_state=42)
    
    # Train test split for regression
    X_train_r, X_test_r, y_r_train, y_r_test = train_test_split(X, y_reg, test_size=0.3, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_train_r_scaled = scaler.fit_transform(X_train_r)
    X_test_r_scaled = scaler.transform(X_test_r)
    
    return X_train_scaled, X_test_scaled, y_c_train, y_c_test, X_train_r_scaled, X_test_r_scaled, y_r_train, y_r_test, scaler, le_gender

def train_models():
    res = load_and_preprocess_data()
    if res[0] is None:
        return
        
    X_train_scaled, X_test_scaled, y_c_train, y_c_test, X_train_r_scaled, X_test_r_scaled, y_r_train, y_r_test, scaler, le_gender = res
    
    print("Training Random Forest Classifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_scaled, y_c_train)
    print(f"Classifier Accuracy: {clf.score(X_test_scaled, y_c_test):.4f}")
    
    print("Training Random Forest Regressor for Broad Jump...")
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_train_r_scaled, y_r_train)
    print(f"Regressor R2: {reg.score(X_test_r_scaled, y_r_test):.4f}")
    
    print("Saving models and preprocessors to disk...")
    # Save objects
    joblib.dump(clf, "rf_classifier.joblib")
    joblib.dump(reg, "rf_regressor.joblib")
    joblib.dump(scaler, "scaler.joblib")
    joblib.dump(le_gender, "le_gender.joblib")
    
    print("Training complete and models saved!")

if __name__ == "__main__":
    train_models()
