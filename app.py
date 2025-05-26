import streamlit as st
from utils.excel_reader import read_gap_assessment
from utils.recommender import generate_recommendations

st.set_page_config(page_title="ISO27001 Insight Tool", layout="wide")
st.title("🔍 ISO27001 Implementation Status Checker")

uploaded_file = st.file_uploader("Upload Gap Assessment Excel File", type="xlsx")

if uploaded_file:
    df = read_gap_assessment(uploaded_file)
    if df.empty:
        st.warning("⚠️ Could not detect the correct format in your file. Please ensure the file has the necessary 'Control' and 'Status' columns.")
    else:
        st.subheader("📋 Current Implementation Overview")
        st.dataframe(df)

        st.subheader("✅ Recommended Next Steps")
        recs = generate_recommendations(df)
        st.dataframe(recs)