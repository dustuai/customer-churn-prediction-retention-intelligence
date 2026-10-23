import pandas as pd
from src.data_cleaning import clean_data, prepare_target
from src.predict import risk_level
from src.retention_strategy import recommend_retention_action

def test_total_charges_conversion():
    df = pd.DataFrame({"customerID":["A","B"],"TotalCharges":["100.5"," "],"Churn":["No","Yes"]})
    out = clean_data(df)
    assert pd.api.types.is_numeric_dtype(out["TotalCharges"])

def test_target_mapping():
    assert prepare_target(pd.DataFrame({"Churn":["No","Yes"]}))["Churn"].tolist() == [0,1]

def test_risk_levels():
    assert risk_level(0.10) == "Low"
    assert risk_level(0.50) == "Medium"
    assert risk_level(0.90) == "High"

def test_recommendation():
    r = recommend_retention_action({"Contract":"Month-to-month","MonthlyCharges":95,"tenure":5,"TechSupport":"No"})
    assert "contract" in r.lower()
