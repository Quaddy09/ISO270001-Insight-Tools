# utils/recommender.py
import openai
import os

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

