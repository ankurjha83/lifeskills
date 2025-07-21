import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

def read_book_inputs(sheet_name='BookInputs', worksheet_index=0, output_path='data/inputs_from_sheets.json'):
    """
    Reads book metadata from a single-row Google Sheet and saves it as a local JSON file.
    Assumes headers are in row 1 and values are in row 2.
    """
    # Define the scope for Google Sheets API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_path = "config/credentials.json"
    print(f"Looking for: {creds_path}")
    print("Exists?", os.path.exists(creds_path))

    # Load credentials
    creds_path = "config/credentials.json"
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Missing credentials file at {creds_path}")

    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    # Open sheet
    sheet = client.open(sheet_name)
    worksheet = sheet.get_worksheet(worksheet_index)

    # Read headers and values (row 1 = headers, row 2 = values)
    headers = worksheet.row_values(1)
    values = worksheet.row_values(2)

    # Create dictionary mapping
    data = {headers[i]: values[i].strip() if i < len(values) else "" for i in range(len(headers))}

    # Optional: parse comma-separated fields into lists
    if "Main Character(s)" in data:
        data["Main Character(s)"] = [x.strip() for x in data["Main Character(s)"].split(",")]

    if "Key Objects" in data:
        data["Key Objects"] = [x.strip() for x in data["Key Objects"].split(",")]

    # Write to local cache
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Book inputs loaded from Google Sheet and saved to {output_path}")
    return data

# Optional test run
if __name__ == "__main__":
    read_book_inputs()
