# Streamlit Application

## Overview

This directory contains the Streamlit interface for the Customer Churn Prediction & Retention Intelligence project.

The application connects the user interface with reusable Python modules for the prediction and retention recommendation functionality implemented in the project.

## Features

Document the features available in the actual application. These may include:

- Customer information inputs
- Churn-related prediction output
- Customer risk-level classification
- Retention recommendations
- Presentation of results through an interactive interface

## Requirements

- Python
- Dependencies listed in the root `requirements.txt`
- Required trained model and preprocessing artifacts
- Required data files, if used by the application

## Installation

From the repository root, install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Use the actual Streamlit entry-point filename.

For example, if the file is `app/streamlit_app.py`:

```bash
streamlit run app/streamlit_app.py
```

Replace the example path with the real filename.

## Source Modules

The application may use modules in `src/` for prediction and retention logic. Keep imports, model paths, and preprocessing consistent with the existing implementation.

## Troubleshooting

- **Import error:** Check the working directory and module paths.
- **Missing model:** Confirm the model artifact exists at the expected location.
- **Missing CSV:** Verify the file paths.
- **Incorrect output:** Check input features, preprocessing, model compatibility, and risk-level logic.

## Limitations

Predictions and recommendations should be evaluated before being used for operational customer retention decisions.
