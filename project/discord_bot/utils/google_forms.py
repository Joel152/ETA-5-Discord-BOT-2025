from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
import logging

logger = logging.getLogger('discord_bot')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

class GoogleFormsAPI:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.credentials = None
        self.service = None

    async def authenticate(self):
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.credentials = pickle.load(token)
                    logger.info("Loaded credentials from token.pickle")

            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                    logger.info("Refreshed expired credentials")
                else:
                    if not os.path.exists(self.credentials_file):
                        logger.error(f"Credentials file not found: {self.credentials_file}")
                        raise FileNotFoundError(f"Credentials file not found: {self.credentials_file}")
                        
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    self.credentials = flow.run_local_server(port=0)
                    logger.info("Generated new credentials")

                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.credentials, token)
                    logger.info("Saved new credentials to token.pickle")

            self.service = build('sheets', 'v4', credentials=self.credentials)
            logger.info("Successfully authenticated with Google Sheets API")
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise

    async def get_latest_responses(self, spreadsheet_id, range_name):
        try:
            if not self.service:
                await self.authenticate()

            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            logger.info(f"Retrieved {len(values)} responses from Google Sheets")
            return values
            
        except Exception as e:
            logger.error(f"Error fetching responses: {e}")
            raise
