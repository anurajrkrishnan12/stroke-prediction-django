# Stroke Prediction Models

This project implements three machine learning algorithms for stroke prediction using the healthcare dataset.

## Models Implemented
- Random Forest Classifier
- XGBoost Classifier
- AdaBoost Classifier

## Data Preprocessing
- Handled missing values (BMI filled with median)
- Encoded categorical variables using Label Encoding
- Scaled features using StandardScaler
- Balanced the imbalanced dataset using SMOTE (Synthetic Minority Over-sampling Technique)

## Model Performance (on test set after SMOTE balancing)
- **Random Forest**: Accuracy ~96%
- **XGBoost**: Accuracy ~96%
- **AdaBoost**: Accuracy ~88%

## Files
- `stroke_prediction.ipynb`: Jupyter notebook with model training code
- `inference.py`: Python script for making predictions on single data points
- `models/`: Directory containing saved models and scaler
  - `random_forest_model.pkl`
  - `xgboost_model.pkl`
  - `adaboost_model.pkl`
  - `scaler.pkl`

## Usage

### Training
Run the Jupyter notebook `stroke_prediction.ipynb` to train the models and save them.

### Inference
Use the `inference.py` script to make predictions on new data.

Example:
```python
from inference import predict_stroke

# Sample patient data
patient_data = {
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

# Get prediction from Random Forest
result = predict_stroke(patient_data, model='random_forest')
print(result)
```

### Data Format
Input data should be a dictionary with the following keys:
- `gender`: 'Male', 'Female', or 'Other'
- `age`: float
- `hypertension`: 0 or 1
- `heart_disease`: 0 or 1
- `ever_married`: 'Single', 'Married', 'Divorced', or 'Widowed'
- `work_type`: 'Private' (Private Sector), 'Self-employed' (Entrepreneur), 'Govt_job' (Public Sector), 'children' (Student), 'Never_worked' (Unemployed)
- `Residence_type`: 'Urban' or 'Rural'
- `avg_glucose_level`: float
- `bmi`: float
- `smoking_status`: 'formerly smoked', 'never smoked', 'smokes', 'Unknown'

## Dependencies
- pandas
- numpy
- scikit-learn
- xgboost
- imbalanced-learn
- joblib

Install with:
```
pip install pandas numpy scikit-learn xgboost imbalanced-learn joblib
```</content>
<parameter name="filePath">d:\PROJECTS\PROJECT_2026\CTS\PROJECTS\Stroke_Prediction\stroke_prediction\ML\README.md