# Aplikasi Format Soal

Aplikasi untuk memformat soal dari file Word ke dalam template tabel dan menguploadnya ke Google Docs.

## Fitur
- Upload file soal dalam format Word (.docx)
- Konversi otomatis ke format tabel terstruktur
- Upload hasil ke Google Docs
- Share link Google Docs dengan permission viewer
- Interface web yang mudah digunakan

## Cara Setup Google Cloud Service Account

1. Buka [Google Cloud Console](https://console.cloud.google.com)
2. Buat project baru atau pilih project yang sudah ada
3. Aktifkan Google Drive API:
   - Buka menu "APIs & Services" -> "Library"
   - Cari "Google Drive API"
   - Klik "Enable"
4. Buat Service Account:
   - Buka menu "APIs & Services" -> "Credentials"
   - Klik "Create Credentials" -> "Service Account"
   - Isi nama service account dan deskripsi
   - Klik "Create"
5. Buat key untuk Service Account:
   - Klik service account yang baru dibuat
   - Buka tab "Keys"
   - Klik "Add Key" -> "Create new key"
   - Pilih format "JSON"
   - Klik "Create". File key akan otomatis terdownload

## Cara Deploy ke Streamlit Cloud

1. Clone repository ini ke GitHub Anda
2. Daftar/login ke [Streamlit Cloud](https://streamlit.io/cloud)
3. Di dashboard Streamlit Cloud:
   - Klik "New app"
   - Pilih repository ini
   - Pilih branch (biasanya main)
   - Pilih file app.py sebagai main file
4. Konfigurasi Secrets:
   - Di app settings, buka bagian "Secrets"
   - Copy seluruh isi file JSON key service account yang sudah didownload
   - Tambahkan ke secrets dengan format:
     ```toml
     [service_account_info]
     type = "service_account"
     project_id = "your-project-id"
     private_key_id = "your-private-key-id"
     private_key = "your-private-key"
     client_email = "your-service-account-email"
     client_id = "your-client-id"
     auth_uri = "https://accounts.google.com/o/oauth2/auth"
     token_uri = "https://oauth2.googleapis.com/token"
     auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
     client_x509_cert_url = "your-cert-url"
     ```
5. Klik "Deploy"

## Format File Input

File Word harus mengikuti format berikut:
```
1. Pertanyaan pertama
A. Pilihan A
B. Pilihan B
C. Pilihan C
D. Pilihan D
E. Pilihan E
Kunci: A

2. Pertanyaan kedua
...dst
```

## Dependencies
Install semua dependencies yang diperlukan:
```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi Secara Lokal
1. Pastikan semua dependencies sudah terinstall
2. Letakkan file service-account.json di folder aplikasi
3. Jalankan aplikasi:
```bash
streamlit run app.py
```

## Keamanan
- Jangan pernah commit file credentials (service-account.json) ke repository
- Gunakan secrets di Streamlit Cloud untuk menyimpan credentials
- Batasi akses API hanya ke domain aplikasi Streamlit
- Update dependencies secara berkala untuk patch keamanan
