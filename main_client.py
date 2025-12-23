import streamlit as st
from app_pages.page_survey import survey_page
import json

with open("questions.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)


st.set_page_config(
    page_title="Collabworx Diagnostic – Survey",
    page_icon="✨",
    layout="wide"
)

# Read client name from URL
params = st.query_params
client_name = params.get("client", ["Unknown"])

survey_page(client_name)
