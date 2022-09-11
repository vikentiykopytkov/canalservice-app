import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1AQEg19yRpER_2s5VxpASdFjXfM1XZ0umpXqr1Fyha2o'
SAMPLE_RANGE_NAME = 'Данные!A2:D'


# Проверка на соответствие данных из таблицы согласно необходимому шаблону
def validate(data: tuple) -> bool:
    RULES = {'0': lambda c:c.isdigit(), '.': lambda c: not c.isdigit() and not c.isalpha()}
    mask='00.00.0000'
    if not data [0].isdigit() or not data [1].isdigit() or not data [2].isdigit() or len(data [3]) != 10:
        return False
    for index, rule in enumerate(mask):
        if not RULES[rule](data [3][index]):
            return False
    return True
        
# Получение данных из Google-таблицы
def get_data():
    creds = None
    if os.path.exists('auth/token.json'):
        creds = Credentials.from_authorized_user_file('auth/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'auth/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('auth/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            return False

        # Обработка данных из Google-таблицы
        data = []
        for row in values:
            try:
                if validate((row [0], row [1], row [2], row [3])):
                    data.append(
                        (
                            int(row [0]), 
                            int(row [1]), 
                            int(row [2]), 
                            datetime.datetime.strptime(row [3], '%d.%m.%Y').date()
                        ))
            except IndexError:
                pass

        return data

    except HttpError:
        return False