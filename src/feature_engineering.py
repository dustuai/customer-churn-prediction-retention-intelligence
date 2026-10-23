import pandas as pd

def add_business_features(df):
    data = df.copy()

    if "tenure" in data.columns:
        data["TenureGroup"] = pd.cut(
            data["tenure"], [-1, 12, 24, 48, float("inf")],
            labels=["0-12", "13-24", "25-48", "49+"]
        )

    service_cols = [
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    existing = [c for c in service_cols if c in data.columns]
    if existing:
        data["ServiceCount"] = data[existing].apply(
            lambda c: c.eq("Yes").astype(int)
        ).sum(axis=1)

    for source, target in [
        ("OnlineSecurity", "HasSecurity"),
        ("TechSupport", "HasSupport"),
        ("OnlineBackup", "HasBackup"),
        ("DeviceProtection", "HasDeviceProtection")
    ]:
        if source in data.columns:
            data[target] = data[source].eq("Yes").astype(int)

    if "Contract" in data.columns:
        data["IsMonthToMonth"] = data["Contract"].eq("Month-to-month").astype(int)

    if "MonthlyCharges" in data.columns:
        data["HighMonthlyCharge"] = (
            data["MonthlyCharges"] >= data["MonthlyCharges"].median()
        ).astype(int)

    return data
