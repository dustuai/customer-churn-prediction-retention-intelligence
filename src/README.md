# Source Code Documentation

## Overview

This directory contains reusable Python modules for the Customer Churn Prediction & Retention Intelligence project.

## Main Modules

### `predict.py`

Documents the prediction functionality, including the model-loading process, required inputs, preprocessing, and risk-level classification implemented in the source code.

### `retention_strategy.py`

Documents the rules used to generate retention recommendations based on the project's implemented logic.

## Usage

The Streamlit application can import reusable functions from these modules. For example, the existing application may use:

```python
from src.predict import risk_level
from src.retention_strategy import recommend_retention_action
```

Keep these imports consistent with the actual module names.

## Development Practices

- Validate user inputs.
- Keep training and inference preprocessing consistent.
- Handle invalid or missing inputs.
- Document risk categories and recommendation rules.
- Test important functions.
