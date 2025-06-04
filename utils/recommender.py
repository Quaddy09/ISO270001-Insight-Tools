import pandas as pd

def generate_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    recommendations = []

    for index, row in df.iterrows():
        control = str(row.get("Control", "")).strip()
        status = str(row.get("Implementation Status", "")).strip().lower()

        if not control or not status:
            continue

        if status in ["not implemented", "no"]:
            recommendations.append({
                "Control": control,
                "Status": status.title(),
                "Recommendation": f"Implement control: {control}"
            })
        elif status in ["partial", "in progress"]:
            recommendations.append({
                "Control": control,
                "Status": status.title(),
                "Recommendation": f"Complete full implementation for control: {control}"
            })
        elif status in ["implemented", "yes"]:
            recommendations.append({
                "Control": control,
                "Status": status.title(),
                "Recommendation": "No action needed"
            })
        else:
            recommendations.append({
                "Control": control,
                "Status": status.title(),
                "Recommendation": "Unknown status — please review manually"
            })

    return pd.DataFrame(recommendations)
