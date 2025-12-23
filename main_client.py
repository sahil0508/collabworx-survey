import streamlit as st
from app_pages.page_survey import survey_page
import json

with open("questions.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

# Read client name from URL
params = {k.lower(): v for k, v in st.query_params.items()}
if not raw_client:
    st.error("Missing ?client= parameter in URL")
    st.stop()
client_name = raw_client[0] if isinstance(raw_client, list) else raw_client
client_name = client_name.strip()

st.set_page_config(
    page_title="Collabworx Diagnostic – Survey",
    page_icon="✨",
    layout="wide"
)

survey_page(client_name)

