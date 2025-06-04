# utils/ai_assistant.py
import os
import openai
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_findings(df: pd.DataFrame) -> str:
    summary = f"The dataset contains {len(df)} controls."
    implemented = df[df['Status'].astype(str).str.lower() == 'implemented']
    not_implemented = df[~df['Status'].astype(str).str.lower().isin(['implemented'])]
    summary += f" Out of these, {len(implemented)} are marked as implemented, and {len(not_implemented)} need attention."
    return summary

def generate_ai_recommendation(df: pd.DataFrame) -> str:
    implemented = df[df['Status'].astype(str).str.lower() == 'implemented']
    not_implemented = df[~df['Status'].astype(str).str.lower().isin(['implemented'])]

    prompt = f"""
    You are an ISO 27001 expert. Based on this data, suggest the top 3 controls to prioritize:
    
    Not Implemented Controls:
    {not_implemented[['Control', 'Description']].head(10).to_string(index=False)}

    Already Implemented Controls:
    {implemented[['Control', 'Description']].head(5).to_string(index=False)}
    
    Provide your suggestions clearly and concisely:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in ISO 27001 gap analysis."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"Error generating AI recommendation: {e}"
