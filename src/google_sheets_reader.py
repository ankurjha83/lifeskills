import os
import json
import google.auth
from googleapiclient.discovery import build

SPREADSHEET_ID = "1t-hgU28nKPZAll0ZOYZa9fvcgcIZ62Qns2LoTab5o-4"
RANGE_NAME = "BookInputs!A1:P2"
OUTPUT_PATH = "data/inputs_from_sheets.json"

def read_book_inputs():
    print("🔐 Loading credentials from environment variable...")
    creds, _ = google.auth.default()

    print("📡 Connecting to Google Sheets API...")
    service = build("sheets", "v4", credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME
    ).execute()

    rows = result.get("values", [])
    if len(rows) < 2:
        print("⚠️ Sheet does not have enough data.")
        return {}

    headers = rows[0]
    values = rows[1]

    inputs = {}
    for key, value in zip(headers, values):
        if key and value:
            norm_key = key.strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
            inputs[norm_key] = value.strip()

    # ✅ Save to JSON
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(inputs, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved inputs to {OUTPUT_PATH}")
    return inputs

if __name__ == "__main__":
    read_book_inputs()
