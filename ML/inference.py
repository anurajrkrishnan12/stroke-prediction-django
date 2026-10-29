import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
import os


# Load models and scaler
rf_model = joblib.load(os.path.join(os.getcwd(), './ML/models/random_forest_model.pkl'))
xgb_model = joblib.load(os.path.join(os.getcwd(), './ML/models/xgboost_model.pkl'))
ada_model = joblib.load(os.path.join(os.getcwd(), './ML/models/adaboost_model.pkl'))
scaler = joblib.load(os.path.join(os.getcwd(), './ML/models/scaler.pkl'))

# Function to preprocess single data point
def preprocess_single_data(data):
    # Convert to DataFrame
    df = pd.DataFrame([data])

    # Encode categorical variables (using the same encoding as training)
    le_gender = LabelEncoder()
    le_gender.fit(['Female', 'Male', 'Other'])
    df['gender'] = le_gender.transform(df['gender'])

    le_married = LabelEncoder()
    le_married.fit(['Single', 'Married', 'Divorced', 'Widowed'])
    df['ever_married'] = le_married.transform(df['ever_married'])

    le_work = LabelEncoder()
    le_work.fit(['Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'])
    df['work_type'] = le_work.transform(df['work_type'])

    le_residence = LabelEncoder()
    le_residence.fit(['Rural', 'Urban'])
    df['Residence_type'] = le_residence.transform(df['Residence_type'])

    le_smoking = LabelEncoder()
    le_smoking.fit(['formerly smoked', 'never smoked', 'smokes', 'Unknown'])
    df['smoking_status'] = le_smoking.transform(df['smoking_status'])

    # Scale the features
    scaled_data = scaler.transform(df)

    return scaled_data

# Function to make predictions
def predict_stroke(data, model='random_forest'):
    processed_data = preprocess_single_data(data)

    models = {
        'random_forest': rf_model,
        'xgboost': xgb_model,
        'adaboost': ada_model
    }

    if model not in models:
        raise ValueError("Model must be 'random_forest', 'xgboost', or 'adaboost'")

    selected_model = models[model]
    prediction = selected_model.predict(processed_data)
    probability = selected_model.predict_proba(processed_data)

    return {
        'model': model,
        'prediction': int(prediction[0]),
        'probability_no_stroke': float(probability[0][0]),
        'probability_stroke': float(probability[0][1])
    }

# Example usage
if __name__ == "__main__":
    # Example patient data
    sample_data = {
        'gender': 'Male',
        'age': 67.0,
        'hypertension': 0,
        'heart_disease': 1,
        'ever_married': 'Married',
        'work_type': 'Private',
        'Residence_type': 'Urban',
        'avg_glucose_level': 228.69,
        'bmi': 36.6,
        'smoking_status': 'formerly smoked'
    }

    # Get predictions from all models
    models_list = ['random_forest', 'xgboost', 'adaboost']
    for model_name in models_list:
        result = predict_stroke(sample_data, model=model_name)
        print(f"\n{model_name.upper()} Prediction:")
        print(f"Stroke Prediction: {'Yes' if result['prediction'] == 1 else 'No'}")
        print(f"Probability of No Stroke: {result['probability_no_stroke']:.2f}")
        print(f"Probability of Stroke: {result['probability_stroke']:.2f}")