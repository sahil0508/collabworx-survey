import streamlit as st
import json
from utils import append_response_to_sheet


def survey_page(client_name):

    if not client_name or client_name == "Unknown":
        st.error("Missing ?client=XYZ in URL")
        return

    st.title("COLLABWORX – Executive Team Diagnostic Survey")

    # Load questions once
    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    # NEW: responses indexed by question number
    responses = {}

    for i, q in enumerate(questions):
        st.subheader(q["text"])
        responses[i] = st.radio(
            label="",
            options=[1, 2, 3, 4],   # change to [1,2,3,4,5] if needed
            horizontal=True,
            key=f"q_{i}"
        )

    if st.button("Submit"):
        append_response_to_sheet(
            responses=responses,
            client_name=client_name,
            questions=questions
        )
        st.success("Thank you! Your responses have been recorded.")
