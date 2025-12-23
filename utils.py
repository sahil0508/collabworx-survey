import os
import json
import pandas as pd
import gspread
from datetime import datetime
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

# -------------------------------------------------------
# Load Google credentials
# -------------------------------------------------------
def get_creds():
    creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)


# -------------------------------------------------------
# Get (or create) worksheet for a client
# -------------------------------------------------------
def get_client_worksheet(client_name: str):
    creds = get_creds()
    gc = gspread.authorize(creds)

    master_sheet_id = os.getenv("MASTER_SHEET_ID")
    sh = gc.open_by_key(master_sheet_id)

    existing_tabs = [ws.title for ws in sh.worksheets()]

    if client_name in existing_tabs:
        return sh.worksheet(client_name)

    # Create new tab for client
    ws = sh.add_worksheet(title=client_name, rows=2000, cols=10)
    return ws


# -------------------------------------------------------
# Append survey responses (LONG FORMAT)
# -------------------------------------------------------
def append_response_to_sheet(responses: dict, client_name: str, questions: list):
    """
    responses: {question_index: score}
    client_name: 'HCL'
    questions: loaded questions.json
    """

    ws = get_client_worksheet(client_name)

    # Ensure headers exist
    headers = ws.row_values(1)
    if not headers:
        headers = [
            "sno",
            "client",
            "question",
            "category",
            "score",
            "timestamp"
        ]
        ws.insert_row(headers, 1)

    # Determine next submission number
    existing_snos = ws.col_values(1)[1:]  # skip header
    sno = max(map(int, existing_snos)) + 1 if existing_snos else 1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows_to_append = []

    for q_index, score in responses.items():
        q = questions[q_index]

        rows_to_append.append([
            sno,
            client_name,          # FULL client name
            q["text"],
            q["category"],
            score,
            timestamp
        ])

    ws.append_rows(rows_to_append, value_input_option="RAW")


# -------------------------------------------------------
# Load client data (for dashboard)
# -------------------------------------------------------
def load_client_data(client_name: str):
    ws = get_client_worksheet(client_name)
    data = ws.get_all_records()
    return pd.DataFrame(data)
