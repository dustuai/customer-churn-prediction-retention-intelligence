def recommend_retention_action(customer):
    actions = []
    if str(customer.get("Contract", "")) == "Month-to-month":
        actions.append("Offer a suitable longer-term contract incentive.")
    if customer.get("MonthlyCharges") is not None and float(customer["MonthlyCharges"]) >= 80:
        actions.append("Review plan value and pricing.")
    if customer.get("tenure") is not None and float(customer["tenure"]) <= 12:
        actions.append("Prioritize early-tenure onboarding and engagement.")
    if str(customer.get("TechSupport", "")) == "No":
        actions.append("Offer proactive technical support or a service bundle.")
    return " ".join(actions[:3]) if actions else "Maintain engagement and monitor risk over time."
