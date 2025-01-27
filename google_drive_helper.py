from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import os
import io
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_EMAIL = 'exo-cbt@exo-cbt-444008.iam.gserviceaccount.com'

def get_google_auth():
    creds = None
    # Token file menyimpan akses dan refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # Jika tidak ada credentials yang valid, minta user untuk login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Simpan credentials untuk run berikutnya
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def upload_to_drive(file_path):
    try:
        creds = get_google_auth()
        service = build('drive', 'v3', credentials=creds)
        
        # Baca file
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Convert ke format yang bisa diupload
        file_metadata = {
            'name': os.path.basename(file_path),
            'mimeType': 'application/vnd.google-apps.document'  # Convert ke Google Docs
        }
        media = MediaIoBaseUpload(
            io.BytesIO(file_content),
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            resumable=True
        )
        
        # Upload file
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink'
        ).execute()
        
        # Set permission untuk service account sebagai viewer
        service.permissions().create(
            fileId=file.get('id'),
            body={
                'type': 'user',
                'role': 'reader',
                'emailAddress': SERVICE_ACCOUNT_EMAIL
            },
            fields='id'
        ).execute()
        
        # Set general access untuk anyone with the link sebagai viewer
        service.permissions().create(
            fileId=file.get('id'),
            body={
                'type': 'anyone',
                'role': 'reader',
                'allowFileDiscovery': False  # File hanya bisa diakses dengan link
            },
            fields='id'
        ).execute()
        
        return file.get('webViewLink')
        
    except Exception as e:
        raise Exception(f"Error uploading to Google Drive: {str(e)}")
