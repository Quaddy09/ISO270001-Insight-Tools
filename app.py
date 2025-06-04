import streamlit as st
import pandas as pd
import difflib
import os
from utils.recommender import generate_recommendations
from utils.ai_assistant import summarize_findings, generate_ai_recommendation

st.set_page_config(page_title="ISO 27001 Gap Assessment Analyzer", layout="wide")
st.title("🔍 ISO 27001 Gap Assessment Analyzer")

st.markdown("**Upload your Gap Assessment Excel File**")
uploaded_file = st.file_uploader("", type=["xlsx"], label_visibility="collapsed")

if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        st.success(f"Sheets found: {sheet_names}")

        # Auto-detect sheets with a likely 'status' column
        def sheet_has_similar_column(sheet_df, target="status"):
            return any(difflib.get_close_matches(target.lower(), [str(c).lower() for c in sheet_df.columns], cutoff=0.6))

        matching_sheets = [sheet for sheet in sheet_names if sheet_has_similar_column(pd.read_excel(xls, sheet_name=sheet))]

        selected_sheet = None
        if matching_sheets:
            selected_sheet = matching_sheets[0]
            st.success(f"Automatically selected sheet: {selected_sheet}")
        else:
            selected_sheet = st.selectbox("Select a sheet to analyze:", sheet_names)

        df = pd.read_excel(xls, sheet_name=selected_sheet)

        # Fuzzy match to find 'status' column
        expected_column = 'status'
        column_matches = difflib.get_close_matches(expected_column.lower(), [str(col).lower() for col in df.columns], cutoff=0.6)

        if not column_matches:
            st.error("❌ Could not find a column similar to 'status'. Please check your sheet.")
        else:
            status_col = column_matches[0]
            st.success(f"Matched column for 'status': {status_col}")

            # Filter or process as needed based on status
            if df[status_col].isnull().all():
                st.warning("The 'status' column appears to be empty.")
            else:
                recommendations = generate_recommendations(df, status_col)
                st.subheader("📋 Summary of Findings")
                st.write(summarize_findings(recommendations))

                if st.checkbox("💡 Generate AI-based Recommendations"):
                    ai_summary = generate_ai_recommendation(recommendations)
                    st.success(ai_summary)

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")