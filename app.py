import streamlit as st
from pipeline import run_pipeline

st.set_page_config(page_title="Retail Insights Assistant")

st.title("🛒 Retail Insights Assistant")

mode = st.selectbox("Select Mode", ["Summary", "Q&A"])
query = st.text_area("Enter your query")

if st.button("Run"):
    if mode == "Summary":
        result = run_pipeline(query, mode="summary")
        st.subheader("Summary")
        st.write(result)
    else:
        answer, validation = run_pipeline(query)
        st.subheader("Answer")
        st.write(answer)
        st.subheader("Validation")
        st.write(validation)
