import datetime
import os.path
from dotenv import load_dotenv
from App.Log.Logs import ferramentas_logger

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
TOKEN_PATH = os.getenv("GOOGLE_TOKEN_PATH")

def autenticar_google():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        ferramentas_logger.info("SUCESSO AO LOGAR NA API")

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH, SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        
        ferramentas_logger.exception(f"ERRO AO LOGAR NA API")

    return creds

def criar_evento_google(titulo, descricao, inicio, fim):
    creds = autenticar_google()
    service = build('calendar', 'v3', credentials=creds)

    evento = {
        'summary': titulo,
        'description': descricao,
        'start': {
            'dateTime': inicio,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': fim,
            'timeZone': 'America/Sao_Paulo',
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 1440}, # Lembra 1 dia antes do evento
                {"method": "popup", "minutes": 60} # e 1h antes também
            ]
        }
    }

    evento = service.events().insert(
        calendarId='primary',
        body=evento
    ).execute()

    return evento.get('htmlLink')

if __name__ == "__main__":
    autenticar_google()