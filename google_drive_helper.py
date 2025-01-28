from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import io
import json
import pickle
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/drive.file']

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
            # Gunakan credentials dari secrets atau file lokal
            try:
                # Import langsung dari file credentials.json
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                
                # Tampilkan URL auth di Streamlit
                auth_url = flow.authorization_url()[0]
                st.markdown("""
                ### Google Drive Authentication
                Ikuti langkah berikut untuk mendapatkan authorization code:
                
                1. Klik link berikut untuk login dengan Google: [Login dengan Google]({})
                
                2. Jika muncul peringatan "Google belum memverifikasi aplikasi ini":
                   - Klik "Advanced" atau "Lanjutan"
                   - Klik "Go to [Nama Project] (unsafe)" atau "Lanjutkan ke [Nama Project] (tidak aman)"
                
                3. Di halaman persetujuan:
                   - Pilih akun Google Anda (jika diminta)
                   - Klik "Continue" atau "Lanjutkan"
                   - Klik "Allow" atau "Izinkan" untuk semua akses yang diminta
                
                4. Setelah itu Anda akan diarahkan ke halaman localhost yang menampilkan pesan error
                   - JANGAN TUTUP halaman tersebut
                   - Copy kode yang muncul di URL halaman tersebut
                   - Kode berada setelah "code=" di URL
                   - Contoh: jika URL-nya http://localhost/?code=4/1AX4XfWi..., maka kodenya adalah 4/1AX4XfWi...
                
                5. Paste kode tersebut di input box di bawah ini
                """.format(auth_url))
                
                # Input box untuk authorization code
                code = st.text_input('Masukkan authorization code:', type='default', 
                                   help="Copy kode dari URL halaman localhost setelah 'code='")
                if code:
                    try:
                        flow.fetch_token(code=code)
                        creds = flow.credentials
                        # Simpan credentials untuk run berikutnya
                        with open('token.pickle', 'wb') as token:
                            pickle.dump(creds, token)
                        st.success('Authentication berhasil!')
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f'Authentication error: {str(e)}. Pastikan kode yang dimasukkan benar dan lengkap.')
                        return None
                else:
                    st.stop()  # Hentikan eksekusi sampai user memasukkan code
                    
            except Exception as e:
                st.error(f"Error dalam autentikasi: {str(e)}")
                return None
    
    return creds

def upload_to_drive(file_path, creds):
    try:
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {'name': 'output.docx'}
        media = MediaFileUpload(file_path, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        file = service.files().create(body=file_metadata, media_body=media, fields='webViewLink').execute()
        
        return file.get('webViewLink')
    
    except Exception as e:
        print(f'Error saat upload ke Google Drive: {str(e)}')
        return None
