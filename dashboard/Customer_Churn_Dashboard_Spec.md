# Power BI Dashboard

## Overview

This directory contains the Power BI report developed for the Customer Churn Prediction & Retention Intelligence project.

The report presents customer churn and retention-related information in an interactive business intelligence interface.

## Report Contents

Document the actual files stored here:

- Power BI report (`.pbix`)
- Custom theme JSON, if used
- Supporting dashboard assets, if required

## Dashboard Pages

List the actual page names from your completed report.

| Page name | Purpose |
|---|---|
| Executive Churn Overview | Provides a high-level summary of customer churn using key performance indicators (KPIs), including total customers, churn rate, and customer       retention metrics. Helps stakeholders quickly understand the overall churn situation and identify areas that may require attention. |
| Customer Churn Analysis | Examines customer churn patterns across demographic groups, service subscriptions, contract types, and billing characteristics. Helps identify customer attributes and service-related patterns associated with higher churn, supporting more informed retention decisions. |
| Customer Segmentation | Segments customers based on relevant characteristics such as tenure, contract type, service usage, and billing behavior. Helps compare customer groups, understand differences in churn patterns, and identify segments that may benefit from targeted engagement and retention strategies. |
| Risk & Prediction | Segments customers based on relevant characteristics such as tenure, contract type, service usage, and billing behavior. Helps compare customer groups, understand differences in churn patterns, and identify segments that may benefit from targeted engagement and retention strategies. |


## Data Sources

Document the CSV files that the report actually uses:

- `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- `telco_churn_clean.csv`

## Opening the Report

1. Install Power BI Desktop.
2. Open the `.pbix` file.
3. Update local CSV paths if necessary.
4. Refresh the data.
5. Check that all visuals, measures, and filters work correctly.

## Screenshots

Store actual screenshots of the finished report in the repository's `images/` folder.

Reference those images from the main `README.md` so visitors can preview the dashboard without downloading the report.

## Sharing

Only share a published Power BI Service link if you have published the report and are authorized to share its contents. Do not publish sensitive data publicly.

## Limitations

Dashboard findings depend on the quality of the data, relationships, measures, and refresh configuration. Risk levels should not be treated as certain predictions of customer behavior.
# Power BI Dashboard Specification

## Source
`data/processed/customer_risk_scores.csv`

## Page 1 — Executive Overview

KPI cards:
- Total Customers
- Churned Customers
- Churn Rate
- High-Risk Customers
- Average Monthly Charges

Charts:
- Churn Rate by Contract
- Churn Rate by Tenure Group
- Churn Rate by Internet Service
- Churn Rate by Payment Method

## Page 2 — Customer Risk Intelligence

Customer table:
- Customer ID
- Tenure
- Contract
- Monthly Charges
- Churn Probability
- Risk Level

Slicers:
- Risk Level
- Contract
- Internet Service
- Payment Method
- Tenure Group

Business question:
**Which customers should the retention team prioritize?**

## Page 3 — Churn Drivers

- Churn by major segment
- Model feature importance
- SHAP global explanation
- High-risk customer counts by segment

## Design

Keep each page focused on one decision. Use consistent percentage formatting and add a note that probabilities are model estimates, not certainties.
