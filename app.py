import streamlit as st
from utils.excel_reader import read_excel_sheets, read_selected_sheet
from utils.recommender import generate_gap_summary, list_missing_controls
from utils.ai_assistant import generate_recommendations

st.set_page_config(page_title="ISO 27001 Gap Assessment Analyzer")
st.title("\U0001F50D ISO 27001 Gap Assessment Analyzer")

def main():
    uploaded_file = st.file_uploader("Upload your Gap Assessment Excel File", type=["xlsx"])
    if not uploaded_file:
        st.info("Please upload an Excel file to begin.")
        return

    try:
        sheets = read_excel_sheets(uploaded_file)
        st.success(f"Sheets found: {sheets}")
    except Exception as e:
        st.error(f"Error reading sheets: {e}")
        return

    sheet_name = st.selectbox("Select a sheet to analyze", sheets)
    try:
        df, status_col = read_selected_sheet(uploaded_file, sheet_name)
    except Exception as e:
        st.error(f"Error reading sheet: {e}")
        return

    if not status_col:
        st.error("❌ Could not find a sheet with an expected 'status' column.")
        return

    st.success(f"✅ Found status column: {status_col}")

    st.subheader("Gap Summary")
    summary = generate_gap_summary(df, status_col)
    st.write(summary)

    st.subheader("Missing Controls")
    missing_df = list_missing_controls(df, status_col)
    st.dataframe(missing_df)

    st.subheader("AI Recommendations")
    try:
        recommendations = generate_recommendations(missing_df)
        for rec in recommendations:
            st.markdown(f"- {rec}")
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")

if __name__ == "__main__":
    main()