# Directory Structure:
# ISO27001 Insight Tool/
# ├── app.py
# ├── requirements.txt
# ├── utils/
# │   └── recommender.py

# File: app.py

import streamlit as st
import pandas as pd
from utils.ai_assistant import generate_recommendations
import os

st.set_page_config(page_title="ISO 27001 Insight Tool", layout="wide")
st.title("🔍 ISO 27001 Gap Assessment Analyzer")

uploaded_file = st.file_uploader("Upload your Gap Assessment Excel File", type=["xlsx"])

if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        st.success(f"Sheets found: {xls.sheet_names}")

        # Attempt to auto-detect the sheet with the gap data
        target_df = None
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            if any("status" in str(col).lower() for col in df.columns):
                target_df = df
                st.subheader(f"📄 Using Sheet: {sheet_name}")
                st.dataframe(df.head())
                break

        if target_df is not None:
            recommendations = generate_recommendations(target_df)
            st.subheader("✅ Recommendations")
            st.dataframe(recommendations)
        else:
            st.warning("❌ Could not find a sheet with expected 'status' column.")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload an Excel file to begin analysis.")
