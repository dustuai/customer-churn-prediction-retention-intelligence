# Jupyter Notebooks

## Overview

This directory contains the notebooks used for analysis, preprocessing, modeling, and evaluation in the Customer Churn Prediction & Retention Intelligence project.

## Notebook Index

List your actual notebooks below.

| Notebook | Description |
|---|---|
|  01_data_understanding | Explores the dataset structure, columns, data types, and initial data quality. |
|  02_data_cleaning | Cleans the dataset by handling missing values, duplicates, and inconsistent data. |
|  03_exploratory_data_analysis | Analyzes customer characteristics and churn patterns using statistics and visualizations. |
|  04_feature_engineering | Prepares and transforms features for machine learning model development.|
|  05_model_training | Trains machine learning models to predict customer churn. |
|  06_model_evaluation | Evaluates model performance using relevant classification metrics.|
|  07_customer_risk_scoring | Classifies customers into risk levels to support retention prioritization. |
|  08_shap_explainability | Uses SHAP to explain model predictions and identify influential features. |


## Execution Order

Follow the actual dependencies between your notebooks. A typical workflow may include:

1. Data inspection and exploration
2. Data cleaning and preparation
3. Feature engineering
4. Model training and evaluation
5. Customer risk output generation

These steps should not be assumed to correspond to separate notebooks unless that matches your project.

## Running the Notebooks

From the repository root:

```bash
jupyter notebook
```

Install dependencies using the root `requirements.txt` before execution.

## Reproducibility

- Run cells in order.
- Check all data and model paths.
- Record relevant model parameters and random seeds.
- Verify that generated files match the documented outputs.
- Avoid committing obsolete outputs or confidential information.

## Outputs

Document the actual files created or updated by the notebooks, including processed CSVs, model artifacts, and evaluation reports.
