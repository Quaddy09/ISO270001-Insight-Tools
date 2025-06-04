import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_findings(df):
    implemented = df[df['Status'].str.lower() == 'implemented']
    partial = df[df['Status'].str.lower() == 'partial']
    not_impl = df[df['Status'].str.lower() == 'not implemented']
    return f"{len(implemented)} controls are fully implemented, {len(partial)} partially implemented, and {len(not_impl)} not implemented."

def generate_ai_recommendation(df):
    try:
        prompt = (
            "You are an ISO 27001 implementation advisor. Given this dataset of controls and statuses, "
            "suggest the top 3 most important actions to prioritize to improve ISO 27001 implementation.\n\n"
        )

        top_rows = df[['Control', 'Status']].dropna().head(20).to_string(index=False)
        prompt += top_rows

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in ISO 27001 implementation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating AI recommendation: {str(e)}"