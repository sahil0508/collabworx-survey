import streamlit as st
from app_pages.page_survey import survey_page
import json

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

st.set_page_config(
    page_title="Collabworx Diagnostic – Survey",
    page_icon="✨",
    layout="wide"
)

# -----------------------------
# Read query params safely
# -----------------------------
params = {k.lower(): v for k, v in st.query_params.items()}

raw_client = params.get("client")
if not raw_client:
    st.error("Missing ?client= parameter in URL")
    st.stop()

client_name = raw_client[0] if isinstance(raw_client, list) else raw_client
client_name = client_name.strip()

# -----------------------------
# Optional: Access key gate
# -----------------------------
required_key = st.secrets.get("SURVEY_ACCESS_KEY")
if required_key:
    raw_key = params.get("key")
    provided_key = raw_key[0] if isinstance(raw_key, list) else raw_key

    if provided_key != required_key:
        st.error("Invalid or missing access key")

