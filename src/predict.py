import joblib
import pandas as pd

def load_model(path):
    return joblib.load(path)

def risk_level(probability, low_cutoff=0.30, high_cutoff=0.70):
    if probability < low_cutoff:
        return "Low"
    if probability < high_cutoff:
        return "Medium"
    return "High"

def predict_customer(model, customer_record):
    X = pd.DataFrame([customer_record])
    probability = float(model.predict_proba(X)[:, 1][0])
    return probability, risk_level(probability)
