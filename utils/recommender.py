def generate_recommendations(df):
    recommendations = []
    for _, row in df.iterrows():
        control = str(row.get("Control", "Unknown"))
        status = str(row.get("Status", "")).lower()

        if status in ["not implemented", "partial"]:
            action = "Review control and implement missing requirements"
        elif status in ["implemented", "complete"]:
            action = "Ensure control is periodically reviewed"
        else:
            action = "Status unclear - verify manually"

        recommendations.append({
            "Control": control,
            "Current Status": row.get("Status", ""),
            "Recommended Action": action
        })

    return recommendations