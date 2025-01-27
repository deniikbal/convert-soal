# Panduan Detail Autentikasi Google Drive

## Langkah 1: Konfigurasi di Google Cloud Console

1. **Persiapan di Google Cloud Console**
   - Buka [Google Cloud Console](https://console.cloud.google.com)
   - Pilih project "exo-cbt-444008"
   - Buka menu "APIs & Services" -> "OAuth consent screen"

2. **Konfigurasi OAuth Consent Screen**
   - Di bagian "Test users"
   - Klik "ADD USERS"
   - Tambahkan email yang akan menggunakan aplikasi
   - Klik "SAVE"

3. **Update Credentials**
   - Buka menu "APIs & Services" -> "Credentials"
   - Cari OAuth 2.0 Client yang ada
   - Klik edit (ikon pensil)
   - Di bagian "Authorized redirect URIs"
   - Tambahkan: `http://localhost:8501/`
   - Klik "SAVE"

4. **Pastikan API Aktif**
   - Buka menu "APIs & Services" -> "Library"
   - Cari "Google Drive API"
   - Pastikan statusnya "Enabled"

## Langkah 2: Mendapatkan Authorization Code

1. **Klik Link Login Google**
   - Kembali ke aplikasi Format Soal
   - Klik link "Login dengan Google"
   - Browser akan membuka halaman login Google

2. **Halaman Peringatan Google**
   - Jika muncul pesan "Google belum memverifikasi aplikasi ini":
   - Klik "Lanjutan" atau "Advanced" di pojok kiri bawah
   - Klik "Lanjutkan ke exo-cbt-444008 (tidak aman)" atau "Go to exo-cbt-444008 (unsafe)"

3. **Halaman Izin Akses**
   - Pilih akun Google yang sudah ditambahkan sebagai test user
   - Pada halaman "exo-cbt-444008 wants to access your Google Account"
   - Scroll ke bawah dan klik "Continue"
   - Centang semua izin yang diminta
   - Klik "Continue" lagi

4. **Dapatkan Kode Autentikasi**
   - Browser akan mengarahkan ke URL seperti:
     ```
     http://localhost:8501/?state=xxxx&code=4/0AeaYSHDKN_KJBs...&scope=...
     ```
   - Copy bagian kode yang ada setelah `code=` dan sebelum `&scope`
   - Contoh: jika URLnya seperti di atas, copy `4/0AeaYSHDKN_KJBs...`

5. **Masukkan Kode ke Aplikasi**
   - Kembali ke aplikasi Format Soal
   - Paste kode yang sudah di-copy ke kotak input "Masukkan authorization code:"
   - Klik Enter atau tekan tombol Submit
   - Tunggu sampai muncul pesan "Authentication berhasil!"

## Troubleshooting

### Jika Muncul "Access blocked: Authorization Error"
1. Pastikan email Anda sudah ditambahkan sebagai test user
2. Pastikan menggunakan email yang sama untuk login
3. Tunggu 5-10 menit setelah menambahkan test user
4. Coba logout dari semua akun Google dan login kembali

### Jika Muncul Error "Invalid Grant"
- Kode autentikasi hanya bisa digunakan sekali
- Klik link login kembali untuk mendapatkan kode baru
- Pastikan menggunakan kode yang baru di-copy

### Jika Muncul Error "Redirect URI Mismatch"
- Pastikan sudah menambahkan `http://localhost:8501/` di Authorized redirect URIs
- Pastikan menggunakan browser yang sama dari awal sampai akhir proses
- Jangan buka link login di browser yang berbeda

## Setelah Autentikasi Berhasil
1. Aplikasi akan refresh otomatis
2. Anda akan bisa melihat form upload file
3. File yang diupload akan otomatis dikonversi dan disimpan di Google Drive
4. Link sharing akan dibuat otomatis dengan akses "Anyone with the link"

## Catatan Penting
File credentials.json dan token.pickle sekarang disimpan di repository untuk memastikan settingan yang sama antara lokal dan production.

## Bantuan
Jika mengalami kesulitan atau error yang tidak tercantum di panduan ini, silakan:
1. Coba logout dari Google Account dan login kembali
2. Hapus file token.pickle (jika ada) dan coba proses autentikasi dari awal
3. Pastikan menggunakan versi browser terbaru
