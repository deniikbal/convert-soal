# Aplikasi Format Soal

Aplikasi untuk memformat soal dari file Word ke dalam template tabel dan menguploadnya ke Google Docs.

## Cara Deploy ke Streamlit Cloud

1. Buat akun di [Streamlit Cloud](https://streamlit.io/cloud)
2. Upload project ke GitHub repository
3. Di dashboard Streamlit Cloud:
   - Klik "New app"
   - Pilih repository yang berisi aplikasi
   - Pilih branch (biasanya main)
   - Pilih file app.py sebagai main file
   - Klik "Deploy"

## File yang Diperlukan
- credentials.json (Google Cloud credentials)
- requirements.txt (sudah disediakan)
- app.py (file utama aplikasi)
- google_drive_helper.py (helper untuk Google Drive integration)

## Persiapan Sebelum Deploy
1. Pastikan semua file berada dalam repository GitHub
2. Di Streamlit Cloud, tambahkan secrets berikut di menu Settings -> Secrets:
```toml
[general]
credentials_json = """isi dengan konten dari file credentials.json"""
```

## Notes
- Credential secrets akan digunakan untuk membuat file credentials.json saat runtime
- Pastikan Google Drive API sudah diaktifkan di Google Cloud Console
- Service account yang digunakan harus memiliki akses ke Google Drive

## Keamanan
- Jangan commit file credentials.json ke repository
- Gunakan secrets di Streamlit Cloud untuk menyimpan credentials
- Batasi akses API hanya ke domain aplikasi Streamlit
