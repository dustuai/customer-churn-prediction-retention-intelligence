from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score,
)

# Project paths
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "processed" / "telco_churn_clean.csv"
MODEL_PATH = ROOT / "models" / "final_model.joblib"

# Use the same customer features exposed by the prediction interface.
FEATURES = [
    "tenure",
    "Contract",
    "InternetService",
    "PaymentMethod",
    "MonthlyCharges",
]
TARGET = "Churn"


def main():
    print("Loading customer churn dataset...")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required = FEATURES + [TARGET]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required dataset columns: {missing}"
        )

    # Keep only the features needed by the prediction interface.
    df = df[required].copy()

    # Convert numeric features safely.
    for col in ["tenure", "MonthlyCharges"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove rows with missing target labels.
    df = df.dropna(subset=[TARGET])

    # Normalize target labels to binary 0/1.
    if df[TARGET].dtype == "object":
        labels = (
            df[TARGET]
            .astype(str)
            .str.strip()
            .str.lower()
        )
        mapping = {
            "yes": 1,
            "no": 0,
            "1": 1,
            "0": 0,
            "true": 1,
            "false": 0,
        }
        df[TARGET] = labels.map(mapping)

    df = df.dropna(subset=[TARGET])
    df[TARGET] = df[TARGET].astype(int)

    if not set(df[TARGET].unique()).issubset({0, 1}):
        raise ValueError(
            "Churn must contain binary labels 0/1 or Yes/No."
        )

    X = df[FEATURES]
    y = df[TARGET]

    if y.nunique() != 2 or y.value_counts().min() < 2:
        raise ValueError(
            "Need at least two examples of each churn class."
        )

    categorical = [
        "Contract",
        "InternetService",
        "PaymentMethod",
    ]
    numeric = ["tenure", "MonthlyCharges"]

    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipe = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),
        (
            "onehot",
            OneHotEncoder(handle_unknown="ignore"),
        ),
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipe, numeric),
        ("cat", categorical_pipe, categorical),
    ])

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestClassifier(
                n_estimators=300,
                min_samples_leaf=3,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ])

    print(f"Dataset rows: {len(df)}")
    print(f"Training features: {FEATURES}")
    print("Splitting data for evaluation...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("Training model...")
    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    print("\nEvaluation results")
    print("------------------")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
    print(f"ROC-AUC:  {roc_auc_score(y_test, probabilities):.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))

    # Refit on all labeled rows before saving for app use.
    print("Training final model on all available labeled data...")
    pipeline.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print(f"\nSaved model successfully:\n{MODEL_PATH}")


if __name__ == "__main__":
    main()