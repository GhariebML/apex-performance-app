import gradio as gr
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

print("Loading models for Gradio Interface...")
try:
    clf = joblib.load("rf_classifier.joblib")
    reg = joblib.load("rf_regressor.joblib")
    scaler = joblib.load("scaler.joblib")
    le_gender = joblib.load("le_gender.joblib")
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}. Please ensure train.py was run first.")

feature_order = [
    'age', 'gender', 'height_cm', 'weight_kg', 'body fat_%',
    'diastolic', 'systolic', 'gripForce', 'sit_and_bend_forward_cm',
    'sit-ups counts', 'broad jump_cm'
]

def predict_body_performance(age, gender, height_cm, weight_kg, body_fat, diastolic, systolic, gripForce, sit_and_bend, sit_ups, broad_jump):
    # Encode Gender
    try:
        gender_encoded = le_gender.transform([gender.upper()])[0]
    except Exception:
        gender_encoded = 1
        
    input_data = pd.DataFrame([{
        'age': age,
        'gender': gender_encoded,
        'height_cm': height_cm,
        'weight_kg': weight_kg,
        'body fat_%': body_fat,
        'diastolic': diastolic,
        'systolic': systolic,
        'gripForce': gripForce,
        'sit_and_bend_forward_cm': sit_and_bend,
        'sit-ups counts': sit_ups,
        'broad jump_cm': broad_jump
    }])
    
    # Scale input
    input_scaled = scaler.transform(input_data)
    
    # Predictions
    pred_class = clf.predict(input_scaled)[0]
    probs = clf.predict_proba(input_scaled)[0]
    pred_jump = reg.predict(input_scaled)[0]
    
    summary = f"Predicted Class: {pred_class}\nEstimated Broad Jump: {round(pred_jump, 1)} cm"
    
    prob_df = pd.DataFrame({
        "class": clf.classes_,
        "probability": probs
    })
    
    return summary, prob_df

def plot_feature_importance(top_n=10):
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    top_n = min(top_n, len(feature_order))
    top_indices = indices[:top_n]
    top_features = [feature_order[i] for i in top_indices]
    top_importances = importances[top_indices]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_features[::-1], top_importances[::-1], color='#00e5c8')
    ax.set_xlabel('Relative Importance')
    ax.set_title(f'Top {top_n} Random Forest Feature Importances')
    plt.tight_layout()
    return fig

# Build the Gradio interface with tabs (User's snippet)
with gr.Blocks() as demo:
    gr.Markdown("## Body Performance AI – Final Project Demo")
    gr.Markdown(
        "This interactive app is powered by the **final trained models in this notebook**. "
        "Use the controls to simulate a participant and view the predicted performance class, "
        "probabilities, and broad jump distance."
    )

    with gr.Tab("Prediction"):
        gr.Markdown("### Enter Participant Measurements")

        with gr.Row():
            with gr.Column():
                age = gr.Slider(18, 80, value=30, step=1, label="Age")
                gender = gr.Radio(["M", "F"], value="M", label="Gender")
                height_cm = gr.Slider(140.0, 200.0, value=170.0, step=0.1, label="Height (cm)")
                weight_kg = gr.Slider(40.0, 130.0, value=70.0, step=0.1, label="Weight (kg)")
                body_fat = gr.Slider(3.0, 45.0, value=22.0, step=0.1, label="Body fat (%)")

            with gr.Column():
                diastolic = gr.Slider(40.0, 130.0, value=80.0, step=1.0, label="Diastolic BP (mmHg)")
                systolic = gr.Slider(70.0, 200.0, value=130.0, step=1.0, label="Systolic BP (mmHg)")
                gripForce = gr.Slider(5.0, 70.0, value=35.0, step=0.5, label="Grip Force")
                sit_and_bend = gr.Slider(-5.0, 60.0, value=15.0, step=0.5, label="Sit and Bend Forward (cm)")
                sit_ups = gr.Slider(0.0, 80.0, value=40.0, step=1.0, label="Sit-ups counts")
                broad_jump = gr.Slider(80.0, 300.0, value=190.0, step=1.0, label="Broad jump (cm)")

        predict_btn = gr.Button("Predict")

        summary_output = gr.Textbox(
            label="Prediction Summary",
            lines=3,
            interactive=False
        )

        proba_plot = gr.BarPlot(
            label="Class Probabilities",
            x="class",
            y="probability",
            x_title="Class",
            y_title="Probability",
            width=500,
            height=350
        )

        predict_btn.click(
            fn=predict_body_performance,
            inputs=[
                age, gender, height_cm, weight_kg, body_fat,
                diastolic, systolic, gripForce, sit_and_bend, sit_ups, broad_jump
            ],
            outputs=[summary_output, proba_plot]
        )

    with gr.Tab("Model Insights"):
        gr.Markdown("### Random Forest Feature Importance")

        top_n_slider = gr.Slider(
            minimum=3,
            maximum=len(feature_order),
            value=10,
            step=1,
            label="Number of top features to display"
        )

        def _plot_importance_wrapper(n):
            return plot_feature_importance(top_n=int(n))

        # Initialize with default top 10 by passing the initial value
        fig_output = gr.Plot(
            label="Top Feature Importances",
            value=_plot_importance_wrapper(top_n_slider.value)
        )

        top_n_slider.change(
            fn=_plot_importance_wrapper,
            inputs=top_n_slider,
            outputs=fig_output
        )

if __name__ == "__main__":
    demo.launch(server_port=7860)
