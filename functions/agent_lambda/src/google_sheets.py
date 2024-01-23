import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import SPREADSHEET_NAME, WORKSHEET

def write_to_sheet(tool, tool_response):

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "drive_client_secret.json", scope
    )
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).get_worksheet(WORKSHEET)
    current_row = sheet.find(tool).row
    print("found in row:", current_row)
    for k, v in tool_response.items():
        current_column = sheet.find(k).col
        sheet.update_cell(current_row, current_column, v)