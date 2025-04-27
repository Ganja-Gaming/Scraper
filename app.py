import streamlit as st
from async_scraper import scrape_linkedin_from_csv
import os

# Streamlit page config
st.set_page_config(page_title="LinkedPickle Pro", page_icon=":pickle:", layout="centered")

# Title
st.markdown(
    """
    <h1 style='text-align: center; color: #39FF14;'>LinkedPickle Pro</h1>
    <h3 style='text-align: center; color: #AAAAAA;'>Scrape LinkedIn profiles like a genius, not a grunt.</h3>
    """,
    unsafe_allow_html=True
)

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file (must have a 'Name' column)", type=["csv"])

if uploaded_file is not None:
    st.success("File uploaded successfully! Ready to scrape.")

    if st.button("Start Scraping", key="start_scrape"):
        with st.spinner("Scraping in progress..."):
            result_file = scrape_linkedin_from_csv(uploaded_file)
        
        if os.path.exists(result_file):
            st.success("Scraping complete! Download your results below:")
            with open(result_file, 'rb') as f:
                st.download_button(
                    label="Download CSV Results",
                    data=f,
                    file_name=result_file,
                    mime="text/csv"
                )
        else:
            st.error("Something went wrong. No results file was generated.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Built by a mad scientist for the chaos of capitalism.</p>", unsafe_allow_html=True)
