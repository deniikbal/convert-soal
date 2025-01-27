from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import os
import io
import json
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_EMAIL = 'exo-cbt@exo-cbt-444008.iam.gserviceaccount.com'

def get_google_auth():
    try:
        # Ambil service account credentials dari secrets
        if 'service_account_info' in st.secrets:
            credentials_dict = st.secrets['service_account_info']
        else:
            # Fallback ke file credentials jika ada
            if os.path.exists('service-account.json'):
                with open('service-account.json', 'r') as f:
                    credentials_dict = json.load(f)
            else:
                raise Exception("Service account credentials tidak ditemukan")
        
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=SCOPES
        )
        
        return credentials
    except Exception as e:
        st.error(f"Error dalam autentikasi: {str(e)}")
        return None

def upload_to_drive(file_path):
    try:
        creds = get_google_auth()
        if not creds:
            raise Exception("Authentication gagal")
            
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
