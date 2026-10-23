from pathlib import Path
import pandas as pd

TARGET = "Churn"
ID_COL = "customerID"

def load_raw_data(path):
    return pd.read_csv(path)

def clean_data(df):
    data = df.copy()
    data.columns = [c.strip() for c in data.columns]
    if "TotalCharges" in data.columns:
        data["TotalCharges"] = pd.to_numeric(data["TotalCharges"], errors="coerce")
    for col in data.select_dtypes(include="object").columns:
        data[col] = data[col].astype("string").str.strip()
    if ID_COL in data.columns:
        data = data.drop_duplicates(subset=[ID_COL], keep="first")
    return data

def prepare_target(df):
    data = df.copy()
    data[TARGET] = data[TARGET].map({"No": 0, "Yes": 1}).astype("int8")
    return data

def save_processed(df, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
