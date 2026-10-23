# Model Card — Customer Churn Prediction

## Purpose
Estimate the probability that a customer belongs to the churn class in the historical Telco dataset.

## Intended use
Customer-risk prioritization, analytics and retention workflow support.

## Not intended for
Automatic termination, denial of service, or irreversible decisions without human review.

## Models
- Logistic Regression
- Random Forest
- XGBoost

## Evaluation

Fill with actual run results:

| Model | Precision | Recall | F1 | Target_Rate |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.6995 | 0.3797 | 0.4922 | 0.1441 |
| Random Forest | 0.7710 | 0.2701| 0.4000 | 0.0930 |
| XGBoost | 0.8194 | 0.1578 | 0.2646 | 0.0511 |

## Threshold
Classification report:

              precision    recall  f1-score   support

           0       0.88      0.76      0.81      1035
           1       0.51      0.71      0.60       374

    accuracy                           0.75      1409
    macro avg       0.70      0.74     0.71      1409
    weighted avg    0.78      0.75     0.76      1409

## Limitations
- Historical observational data does not prove causation.
- Patterns may not generalize to another telecom population.
- Retention recommendations are hypotheses.
- Model performance can drift over time.
- Probability is not certainty.
