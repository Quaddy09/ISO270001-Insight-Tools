# utils/recommender.py
import openai
import os
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_gap_with_ai(df):
    """
    Analyze the provided DataFrame and generate recommendations only for controls
    that seem to have missing or weak implementation based on textual analysis.
    """
    incomplete_rows = []
    for i, row in df.iterrows():
        row_text = " ".join(str(cell) for cell in row if pd.notna(cell)).lower()
        if not row_text.strip():
            continue  # skip fully empty rows

        # Heuristic: if the row does NOT contain strong evidence of implementation
        # (e.g., lacks words like "implemented", "completed", etc.)
        if not any(keyword in row_text for keyword in ["implemented", "completed", "evidence", "available", "done"]):
            incomplete_rows.append(row)

    # Convert incomplete rows to string representation for AI input
    prompt_rows = "\n".join([str(row.to_dict()) for row in incomplete_rows])

    if not prompt_rows:
        return "✅ All Annex A controls in this sheet appear to be implemented or documented."

    prompt = f"""
You are an ISO 27001 expert. Based on the following rows of Annex A controls,
identify gaps and suggest what actions the organization should take to comply:

{prompt_rows}

Provide structured, actionable recommendations.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cybersecurity and ISO 27001 consultant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ AI analysis failed: {str(e)}"

def generate_gap_summary(df):
    """
    Basic summary: Count the number of controls that appear implemented vs. missing.
    """
    implemented, missing = 0, 0
    for i, row in df.iterrows():
        row_text = " ".join(str(cell) for cell in row if pd.notna(cell)).lower()
        if not row_text.strip():
            continue
        if any(keyword in row_text for keyword in ["implemented", "completed", "evidence", "available", "done"]):
            implemented += 1
        else:
            missing += 1
    return f"✅ Implemented: {implemented}  |  ❌ Missing or Weak: {missing}"

def list_missing_controls(df):
    """
    Return a short list of the Annex A controls that are likely incomplete.
    """
    incomplete = []
    for i, row in df.iterrows():
        row_text = " ".join(str(cell) for cell in row if pd.notna(cell)).lower()
        if not row_text.strip():
            continue
        if not any(keyword in row_text for keyword in ["implemented", "completed", "evidence", "available", "done"]):
            if row[0] and isinstance(row[0], str):
                incomplete.append(row[0])
            elif row.get("Annex"):
                incomplete.append(row.get("Annex"))

    if not incomplete:
        return ["✅ All controls appear addressed."]

    return incomplete