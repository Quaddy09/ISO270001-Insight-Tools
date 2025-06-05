def generate_gap_summary(df, status_col):
    if not status_col or status_col not in df.columns:
        return "No status column found. Cannot generate summary."
    return df[status_col].value_counts(dropna=False).to_dict()

def list_missing_controls(df, status_col):
    if not status_col or status_col not in df.columns:
        return []
    mask = df[status_col].astype(str).str.lower().str.contains(
        r"\b(not implemented|missing|no)\b", na=False, regex=True
    )
    return df[mask]
