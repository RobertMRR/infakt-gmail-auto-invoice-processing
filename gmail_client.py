import os.path
from defaults import SCOPES
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


creds = None

if os.path.exists(("token.json")):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    
try:
    service = build("gmail", "v1", credentials=creds)
    result = service.users().messages().list(userId="me", labelIds=["INBOX"], q="after:2025/10/28 before:2025/10/30").execute()
    mails = result.get("messages",[])
    first_mail_id = mails[0]["id"]
    msg_info = service.users().messages().get(userId="me", id=first_mail_id).execute()
    print(msg_info.get("snippet",[]))

except HttpError as e:
    print(f"some shit happened: {e}")