# Stroke Prediction System

A web application that predicts a person's risk of stroke using machine learning, and connects patients with verified doctors for online consultation. Built with **Django** and three ML models (**Random Forest, XGBoost, AdaBoost**) trained on the Kaggle Healthcare Stroke dataset.

> **Disclaimer:** This project is for learning and demonstration only. It is not a medical device and must not be used for real diagnosis or treatment decisions.

---

## Features

### For patients (users)
- Register, log in, and manage a profile
- Enter health details and get an instant stroke risk prediction with probability scores
- View past predictions in a prediction history page
- Request a doctor consultation based on a prediction result
- Track consultation status (pending, approved, rejected)
- Forgot/reset password and delete account options

### For doctors
- Register with qualification, specialization, experience, and a proof document upload
- Log in only after admin approval
- Dashboard showing assigned consultations
- Reply to patients with advice and a meeting link

### For admin
- View all registered users and all predictions
- Approve or reject doctor registrations after checking their proof documents
- Approve or reject consultation requests, which assigns an approved doctor

---

## Machine Learning

**Dataset:** `healthcare-dataset-stroke-data.csv` (patient records with stroke outcome)

**Input features:** gender, age, hypertension, heart disease, marital status, work type, residence type, average glucose level, BMI, smoking status

**Preprocessing**
- Missing BMI values filled with the median
- Categorical variables converted with Label Encoding
- Features scaled with StandardScaler
- Class imbalance handled with SMOTE

**Model performance (test set after SMOTE balancing)**

| Model          | Accuracy |
|----------------|----------|
| Random Forest  | ~96%     |
| XGBoost        | ~96%     |
| AdaBoost       | ~88%     |

The training notebooks are in the `ML/` folder, and `ML/inference.py` is used by the web app to make predictions.

---

## Tech Stack

- **Backend:** Python, Django 3.2
- **Machine Learning:** scikit-learn, XGBoost, imbalanced-learn, pandas, NumPy, joblib
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite

---

## Project Structure

```
stroke_prediction12/
├── manage.py
├── ML/
│   ├── healthcare-dataset-stroke-data.csv
│   ├── stroke_prediction.ipynb
│   ├── stroke-prediction-xgboost-97.ipynb
│   ├── inference.py
│   └── models/            # saved models and scaler (.pkl)
├── stroke_prediction/     # Django app: views, models, urls, settings
├── templates/             # HTML pages
└── static/                # CSS, JS, images
```

---

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/anurajrkrishnan12/stroke-prediction-django.git
   cd stroke-prediction-django
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install the requirements**
   ```bash
   pip install django==3.2.7 scikit-learn xgboost imbalanced-learn pandas numpy joblib pillow
   ```

4. **Create the database**
   ```bash
   python manage.py migrate
   ```

5. **Start the server**
   ```bash
   python manage.py runserver
   ```

6. Open **http://127.0.0.1:8000** in your browser.

> The database file and uploaded doctor documents are not included in this repository, so register new users and doctors to try the app.

**Demo admin login** (hard-coded for this demo project): email `admin@gmail.com`, password `admin`

---

## Using the prediction model directly

```python
from inference import predict_stroke

patient = {
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

print(predict_stroke(patient, model='random_forest'))
```

---

## Future Improvements

- Hash passwords and move admin credentials out of the code
- Use environment variables for secret keys and settings
- Add email notifications for consultation updates
- Deploy the app online

---

## Author

**Anuraj R**
BSc Computer Science, School of Technology and Applied Science (STAS), Kochi
[LinkedIn](https://www.linkedin.com/in/anuraj-r-3b182a351) | [GitHub](https://github.com/anurajrkrishnan12)
