def generate_recommendations(missing_df):
    if missing_df.empty:
        return ["No recommendations due to lack of missing data."]

    recommendations = []
    for i, row in missing_df.iterrows():
        context = row.to_dict()
        title = context.get("Control") or context.get("Title") or f"Item {i+1}"
        details = context.get("Description") or context.get("Details") or ""
        responsible = context.get("Responsible") or "a responsible person"
        rec = (
            f"Consider implementing '{title}'."
            f"{' ' + details if details else ''} "
            f"Ensure proper documentation and assign {responsible} to ensure compliance."
        ).strip()
        recommendations.append(rec)
    return recommendations