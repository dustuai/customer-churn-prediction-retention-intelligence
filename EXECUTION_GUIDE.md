# Project Execution Guide

This guide explains how to set up and run the Customer Churn Prediction & Retention Intelligence project.

## 1. Prerequisites

Install the following tools as needed:

- Python, using a version compatible with the project's dependencies
- Git
- Jupyter Notebook or JupyterLab
- Power BI Desktop for the `.pbix` report
- A SQL database or client only if the project's SQL workflow requires one

## 2. Clone the Repository

```bash
git clone https://github.com/dustuai/customer-churn-prediction-retention-intelligence.git
cd customer-churn-prediction-retention-intelligence
```

## 3. Set Up Python

Create a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Verify the Data Files

Check that the required CSV files exist in their documented locations:

- `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- `telco_churn_clean.csv`
- `customer_risk_scores.csv`

Their exact paths should match the code and Power BI data source configuration.

## 5. Execute the Notebooks

Launch Jupyter:

```bash
jupyter notebook
```

Open the notebooks in `notebooks/`.

Follow the actual dependency order of the notebooks. Confirm the input data paths and inspect any model artifacts or processed CSVs that must exist before execution.

## 6. Run the Streamlit Application

Use the real entry-point filename from `app/`.

Example:

```bash
streamlit run app/streamlit_app.py
```

Replace the example filename with the actual file in the repository.

Confirm that the model artifacts, import paths, and required input data are available.

## 7. Open the Power BI Report

1. Open the `.pbix` file in `dashboard/`.
2. Update data source paths if they reference another computer.
3. Refresh the data.
4. Confirm that the visuals and measures load correctly.

## 8. Run Tests

Inspect the tests in `tests/` and follow their documented requirements.

If the project uses pytest, run:

```bash
python -m pytest tests/
```

This command assumes pytest is installed and that the tests are compatible with the project's current environment.

## 9. Troubleshooting

### Missing files

Confirm that the files exist and that relative paths are resolved from the intended working directory.

### Module import errors

Run commands from the project root and check the Python import structure.

### Model loading errors

Check the model file path and compatible library versions. Ensure that the model and preprocessing artifacts match.

### Power BI refresh errors

Update the source file paths and verify the CSV schema.

### Dependency errors

Activate the correct virtual environment and reinstall the required packages.

## 10. Reproducibility

For reproducible results, document the Python version, dependency versions, random seeds, data source, notebook execution order, and model configuration where applicable.
