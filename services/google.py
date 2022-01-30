import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd

from config.settings.base import SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME


class GoogleSheeet():
    
    def __init__(self, worksheet_id, sheet_name, cells_range=None):
        self.creds = None
        self.folder_credentials = 'services/auth'
        self.client_secret_file = 'client_secret.json'
        self.worksheet_id = worksheet_id
        self.range = f'{sheet_name}'
        if cells_range is not None:
            self.range =+ f'!{cells_range}'
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.authenticate()

    def authenticate(self):
        token_path = os.path.join(self.folder_credentials, 'token.json')
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, self.scopes)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                client_secret_path = os.path.join(self.folder_credentials, self.client_secret_file)
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, self.scopes)
                self.creds = flow.run_local_server(port=0)
                with open(token_path, 'w') as token:
                    token.write(self.creds.to_json())

    def get_data(self):
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.worksheet_id, range=self.range).execute()
            values = result.get('values', [])
            return values
        except HttpError as err:
            print(err)
                    

    def to_dataframe(self):
        sheet_data = self.get_data()
        df = pd.DataFrame(sheet_data, columns=sheet_data.pop(0))
        df.PRICE = df.PRICE.apply(pd.to_numeric, errors='coerce')
        return df