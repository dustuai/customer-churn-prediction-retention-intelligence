from pathlib import Path
import sys

import joblib
import pandas as pd
import streamlit as st

# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.predict import risk_level
from src.retention_strategy import recommend_retention_action

MODEL_PATH = ROOT / "models" / "final_model.joblib"

st.set_page_config(
    page_title="Churn Intelligence | Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 2. CUSTOM COLORFUL THEME
# ============================================================

st.markdown(
    """
    <style>
    /* Main page background */
    .stApp {
        background:
            radial-gradient(
                ellipse at 5% 5%,
                rgba(129, 140, 248, 0.20),
                transparent 36%
            ),
            radial-gradient(
                ellipse at 95% 15%,
                rgba(45, 212, 191, 0.16),
                transparent 32%
            ),
            linear-gradient(
                135deg,
                #f5f3ff 0%,
                #eff6ff 48%,
                #ecfeff 100%
            );
        color: #172554;
    }

    [data-testid="stHeader"] {
        background: rgba(245, 243, 255, 0.75);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #eef2ff 0%,
            #f0fdfa 100%
        );
        border-right: 1px solid #dbeafe;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(
            120deg,
            #312e81 0%,
            #4338ca 45%,
            #0891b2 100%
        );
        padding: 34px;
        border-radius: 22px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 12px 32px rgba(67, 56, 202, 0.20);
    }

    .hero h1 {
        color: #ffffff !important;
        font-size: 2.25rem;
        font-weight: 800;
        margin: 0 0 10px 0;
    }

    .hero p {
        color: #e0f2fe !important;
        font-size: 1rem;
        margin: 0;
        line-height: 1.7;
    }

    .hero-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.16);
        color: #ffffff;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        margin-bottom: 14px;
        border: 1px solid rgba(255,255,255,0.25);
    }

    /* Section headings */
    .section-heading {
        color: #312e81;
        font-size: 1.3rem;
        font-weight: 800;
        margin-top: 18px;
        margin-bottom: 14px;
    }

    .section-caption {
        color: #64748b;
        margin-top: -8px;
        margin-bottom: 18px;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.90);
        border: 1px solid #e0e7ff;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 5px 18px rgba(49, 46, 129, 0.07);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #312e81;
        font-weight: 800;
    }

    /* White panels */
    .panel {
        background: rgba(255,255,255,0.94);
        border: 1px solid #e0e7ff;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 5px 20px rgba(49,46,129,0.05);
    }

    .panel h3 {
        color: #312e81;
        margin-top: 0;
    }

    /* Risk labels */
    .risk {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 10px;
        font-size: 0.95rem;
        font-weight: 800;
    }

    .risk-low {
        background: #d1fae5;
        color: #065f46;
    }

    .risk-medium {
        background: #fef3c7;
        color: #92400e;
    }

    .risk-high {
        background: #fee2e2;
        color: #991b1b;
    }

    .muted {
        color: #64748b;
        font-size: 0.88rem;
        line-height: 1.6;
    }

    /* Inputs */
    div[data-baseweb="select"] > div {
        border-radius: 10px;
        border-color: #c7d2fe;
    }

    div[data-testid="stNumberInput"] input {
        border-radius: 10px;
    }

    /* Buttons */
    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 11px;
        font-weight: 700;
        min-height: 46px;
        transition: all 0.2s ease;
    }

    div.stFormSubmitButton > button[kind="primary"] {
        background: linear-gradient(90deg, #4f46e5, #0891b2);
        border: none;
        color: white;
    }

    div.stFormSubmitButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #4338ca, #0e7490);
        color: white;
    }

    /* Dividers and tables */
    hr {
        border-color: #dbeafe;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #e0e7ff;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.82rem;
        padding-top: 22px;
        line-height: 1.7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 3. LOAD MODEL
# ============================================================

@st.cache_resource
def load_model(model_path, modified_time):
    return joblib.load(model_path)


if not MODEL_PATH.exists():
    st.error(
        "Model not found. Train your model first and save it to "
        "models/final_model.joblib."
    )
    st.info("Expected model path: " + str(MODEL_PATH))
    st.stop()

try:
    model = load_model(
        str(MODEL_PATH),
        MODEL_PATH.stat().st_mtime,
    )
except Exception as exc:
    st.error(
        "The saved model could not be loaded. "
        "Check the scikit-learn version used during training."
    )
    st.exception(exc)
    st.stop()

if not hasattr(model, "predict_proba"):
    st.error(
        "The saved model does not support predict_proba(). "
        "Please train a compatible classification pipeline."
    )
    st.stop()

# ============================================================
# 4. HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <span class="hero-tag">CUSTOMER ANALYTICS · MACHINE LEARNING</span>
        <h1>📊 Customer Churn Intelligence</h1>
        <p>
            Predict churn risk, explore customer profiles, and support
            smarter retention decisions with a machine-learning workflow.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 5. SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 💠 Intelligence Hub")
    st.caption("Customer retention workspace")
    st.divider()

    st.markdown("### 🎯 Risk classification")
    st.markdown(
        """
        <span class="risk risk-low">Low · &lt; 30%</span>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        """
        <span class="risk risk-medium">Medium · 30–69%</span>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        """
        <span class="risk risk-high">High · ≥ 70%</span>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### 🧠 About this project")
    st.write(
        "A customer churn prediction and retention decision-support "
        "application built with Python, scikit-learn, pandas, and Streamlit."
    )

    st.markdown("### 🔍 How to use")
    st.write(
        "1. Enter a customer profile.\n"
        "2. Select Analyze Customer.\n"
        "3. Review the predicted probability.\n"
        "4. Consider the suggested retention actions."
    )

    st.divider()
    st.caption(
        "Portfolio demonstration. Predictions are estimates, "
        "not guarantees of future customer behavior."
    )

# ============================================================
# 6. CUSTOMER INPUT FORM
# ============================================================

st.markdown(
    '<div class="section-heading">01 · Customer Profile</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Enter the customer details for an individual risk assessment.'
    '</div>',
    unsafe_allow_html=True,
)

with st.form("customer_profile_form"):
    st.markdown("#### 💳 Subscription and Billing")

    c1, c2, c3 = st.columns(3)

    with c1:
        tenure = st.number_input(
            "Tenure (months)",
            min_value=0,
            max_value=120,
            value=8,
            step=1,
        )
        contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"],
        )

    with c2:
        monthly = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            max_value=500.0,
            value=85.0,
            step=5.0,
        )
        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )

    with c3:
        internet = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"],
        )
        paperless = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"],
        )

    st.divider()
    st.markdown("#### 👤 Customer Characteristics")

    c1, c2, c3 = st.columns(3)

    with c1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior = st.selectbox("Senior Citizen", [0, 1])

    with c2:
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])

    with c3:
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        multiple = st.selectbox(
            "Multiple Lines",
            ["Yes", "No", "No phone service"],
        )

    st.divider()
    st.markdown("#### 🛠️ Service Configuration")

    service_options = ["Yes", "No", "No internet service"]

    c1, c2, c3 = st.columns(3)

    with c1:
        security = st.selectbox("Online Security", service_options)
        backup = st.selectbox("Online Backup", service_options)

    with c2:
        device = st.selectbox("Device Protection", service_options)
        tech = st.selectbox("Tech Support", service_options)

    with c3:
        stream_tv = st.selectbox("Streaming TV", service_options)
        stream_movies = st.selectbox("Streaming Movies", service_options)

    submitted = st.form_submit_button(
        "✨ Analyze Customer Churn Risk",
        type="primary",
        use_container_width=True,
    )

# ============================================================
# 7. CREATE CUSTOMER RECORD AND PREDICT
# ============================================================

if submitted:
    record = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": device,
        "TechSupport": tech,
        "StreamingTV": stream_tv,
        "StreamingMovies": stream_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": tenure * monthly,
        "TenureGroup": (
            "0-12" if tenure <= 12 else
            "13-24" if tenure <= 24 else
            "25-48" if tenure <= 48 else
            "49+"
        ),
        "ServiceCount": sum(
            value == "Yes"
            for value in [
                phone,
                multiple,
                security,
                backup,
                device,
                tech,
                stream_tv,
                stream_movies,
            ]
        ),
        "HasSecurity": int(security == "Yes"),
        "HasSupport": int(tech == "Yes"),
        "HasBackup": int(backup == "Yes"),
        "HasDeviceProtection": int(device == "Yes"),
        "IsMonthToMonth": int(contract == "Month-to-month"),
        "HighMonthlyCharge": int(monthly >= 70),
    }

    input_df = pd.DataFrame([record])

    try:
        # Align inputs to the model's original feature names if available.
        expected_features = getattr(model, "feature_names_in_", None)

        if expected_features is not None:
            expected_features = list(expected_features)

            missing_features = [
                col for col in expected_features
                if col not in input_df.columns
            ]

            if missing_features:
                st.error(
                    "The customer form does not contain all features "
                    "required by the trained model."
                )
                st.write("Missing features:", missing_features)
                st.info(
                    "Retrain the model with the same feature schema as "
                    "the form, or update the form to match the training data."
                )
                st.stop()

            input_df = input_df[expected_features]

        probability_values = model.predict_proba(input_df)

        if probability_values.shape[1] != 2:
            st.error(
                "Expected a binary classification model with two "
                "probability columns."
            )
            st.stop()

        classes = list(getattr(model, "classes_", [0, 1]))

        if 1 not in classes:
            st.error(
                "The trained model does not contain the expected churn "
                "class label 1."
            )
            st.stop()

        churn_column = classes.index(1)
        probability = float(probability_values[0, churn_column])

        if not 0.0 <= probability <= 1.0:
            st.error("The model returned an invalid probability.")
            st.stop()

    except Exception as exc:
        st.error(
            "Prediction failed. Check model compatibility and the "
            "input feature schema."
        )
        st.exception(exc)
        st.stop()

    # Use the same probability thresholds in the result and sidebar.
    if probability < 0.30:
        risk = "Low"
        risk_class = "risk-low"
        risk_message = (
            "The model estimates a lower churn probability. "
            "Continue monitoring customer experience and engagement."
        )
        risk_icon = "🟢"

    elif probability < 0.70:
        risk = "Medium"
        risk_class = "risk-medium"
        risk_message = (
            "The model estimates a moderate churn probability. "
            "Review service experience and possible friction points."
        )
        risk_icon = "🟠"

    else:
        risk = "High"
        risk_class = "risk-high"
        risk_message = (
            "The model estimates a higher churn probability. "
            "Prioritize a review of customer needs and unresolved issues."
        )
        risk_icon = "🔴"

    # ========================================================
    # 8. RESULTS DASHBOARD
    # ========================================================

    st.divider()
    st.markdown(
        '<div class="section-heading">02 · Prediction Dashboard</div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3 = st.columns(3)

    with k1:
        st.metric(
            "Estimated Churn Probability",
            f"{probability:.1%}",
        )

    with k2:
        st.metric(
            "Customer Risk Level",
            f"{risk_icon} {risk}",
        )

    with k3:
        st.metric(
            "Customer Tenure",
            f"{tenure} months",
        )

    st.markdown(
        f"""
        <div class="panel">
            <span class="risk {risk_class}">{risk_icon} {risk} Risk</span>
            <h3 style="margin-top:16px;">Customer Risk Assessment</h3>
            <p style="color:#475569;line-height:1.7;">
                {risk_message}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Probability Visualization")
    st.progress(
        int(round(probability * 100)),
        text=f"Estimated churn probability: {probability:.1%}",
    )

    st.caption(
        "Risk bands are configurable business thresholds, not universal "
        "industry standards. Probability quality depends on model validation."
    )

    # ========================================================
    # 9. RETENTION INTELLIGENCE
    # ========================================================

    st.markdown(
        '<div class="section-heading">03 · Retention Intelligence</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown("#### 🎯 Suggested Retention Action")

        try:
            recommendation = recommend_retention_action(record)
            st.info(recommendation)
        except Exception as exc:
            st.warning(
                "The retention recommendation could not be generated."
            )
            st.caption(str(exc))

        st.markdown("#### 📌 Customer Review Checklist")

        review_items = []

        if contract == "Month-to-month":
            review_items.append(
                "Review whether a longer-term contract provides genuine value."
            )

        if tenure <= 12:
            review_items.append(
                "Review onboarding, early experience, and unresolved issues."
            )

        if tech == "No" and internet != "No":
            review_items.append(
                "Check whether the customer needs technical support."
            )

        if security == "No" and internet != "No":
            review_items.append(
                "Check whether the customer understands available security services."
            )

        if payment == "Electronic check":
            review_items.append(
                "Review billing experience and any payment-related complaints."
            )

        if not review_items:
            review_items.append(
                "Review recent engagement, support history, and customer feedback."
            )

        for item in review_items:
            st.markdown(f"- {item}")

        st.caption(
            "These are review prompts based on the entered profile. "
            "They are not explanations of the model's internal reasoning."
        )

    with right:
        st.markdown("#### 🧾 Customer Snapshot")

        snapshot = pd.DataFrame(
            {
                "Attribute": [
                    "Contract",
                    "Internet Service",
                    "Payment Method",
                    "Monthly Charges",
                    "Tenure",
                    "Tech Support",
                    "Paperless Billing",
                ],
                "Value": [
                    contract,
                    internet,
                    payment,
                    f"{monthly:.2f}",
                    f"{tenure} months",
                    tech,
                    paperless,
                ],
            }
        )

        st.dataframe(
            snapshot,
            hide_index=True,
            use_container_width=True,
        )

    # ========================================================
    # 10. EXPORT CUSTOMER ASSESSMENT
    # ========================================================

    st.markdown(
        '<div class="section-heading">04 · Export Assessment</div>',
        unsafe_allow_html=True,
    )

    result = {
        **record,
        "ChurnProbability": round(probability, 6),
        "RiskLevel": risk,
    }

    result_csv = pd.DataFrame([result]).to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Customer Assessment (CSV)",
        data=result_csv,
        file_name="customer_churn_assessment.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.caption(
        "The export contains the submitted customer profile, "
        "predicted probability, and assigned risk band."
    )

# ============================================================
# 11. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <strong>Customer Churn Intelligence</strong><br>
        Machine Learning · Customer Analytics · Retention Decision Support<br>
        Portfolio demonstration — not a guarantee of future customer behavior.
    </div>
    """,
    unsafe_allow_html=True,
)