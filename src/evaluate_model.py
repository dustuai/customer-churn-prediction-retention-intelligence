import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix
)

def evaluate_binary_classifier(model, X_test, y_test, threshold=0.5):
    p = model.predict_proba(X_test)[:, 1]
    yhat = (p >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, yhat).ravel()
    return {
        "threshold": threshold,
        "accuracy": accuracy_score(y_test, yhat),
        "precision": precision_score(y_test, yhat, zero_division=0),
        "recall": recall_score(y_test, yhat, zero_division=0),
        "f1": f1_score(y_test, yhat, zero_division=0),
        "roc_auc": roc_auc_score(y_test, p),
        "pr_auc": average_precision_score(y_test, p),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)
    }

def threshold_table(model, X_test, y_test, thresholds=None):
    if thresholds is None:
        thresholds = np.arange(0.20, 0.81, 0.05)
    p = model.predict_proba(X_test)[:, 1]
    rows = []
    for t in thresholds:
        yhat = (p >= t).astype(int)
        rows.append({
            "threshold": round(float(t), 2),
            "precision": precision_score(y_test, yhat, zero_division=0),
            "recall": recall_score(y_test, yhat, zero_division=0),
            "f1": f1_score(y_test, yhat, zero_division=0),
            "target_rate": yhat.mean()
        })
    return pd.DataFrame(rows)
