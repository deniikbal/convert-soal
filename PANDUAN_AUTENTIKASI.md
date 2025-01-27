# Panduan Detail Autentikasi Google Drive

## Cara Mendapatkan Authorization Code

1. **Klik Link Login Google**
   - Klik link "Login dengan Google" yang muncul di aplikasi
   - Browser akan membuka halaman login Google

2. **Halaman Peringatan Google**
   - Jika muncul pesan "Google belum memverifikasi aplikasi ini":
   - Klik "Lanjutan" atau "Advanced" di pojok kiri bawah
   - Klik "Lanjutkan ke exo-cbt-444008 (tidak aman)" atau "Go to exo-cbt-444008 (unsafe)"

3. **Halaman Izin Akses**
   - Pilih akun Google Anda
   - Pada halaman "exo-cbt-444008 wants to access your Google Account"
   - Scroll ke bawah dan klik "Continue"
   - Centang semua izin yang diminta
   - Klik "Continue" lagi

4. **Dapatkan Kode Autentikasi**
   - Browser akan mengarahkan ke URL seperti:
     ```
     http://localhost/?state=xxxx&code=4/0AeaYSHDKN_KJBs...&scope=...
     ```
   - Copy bagian kode yang ada setelah `code=` dan sebelum `&scope`
   - Contoh: jika URLnya seperti di atas, copy `4/0AeaYSHDKN_KJBs...`

5. **Masukkan Kode ke Aplikasi**
   - Kembali ke aplikasi Format Soal
   - Paste kode yang sudah di-copy ke kotak input "Masukkan authorization code:"
   - Klik Enter atau tekan tombol Submit
   - Tunggu sampai muncul pesan "Authentication berhasil!"

## Tips Penting
- Pastikan meng-copy keseluruhan kode authorization (biasanya cukup panjang)
- Jangan tutup browser sebelum selesai meng-copy kode
- Jika terjadi error, ulangi proses dari awal dengan mengklik link login kembali

## Troubleshooting

### Jika Muncul Error "Invalid Grant"
- Kode autentikasi hanya bisa digunakan sekali
- Klik link login kembali untuk mendapatkan kode baru
- Pastikan menggunakan kode yang baru di-copy

### Jika Muncul Error "Redirect URI Mismatch"
- Pastikan menggunakan browser yang sama dari awal sampai akhir proses
- Jangan buka link login di browser yang berbeda

### Jika Halaman Localhost Error
- Ini adalah normal dan memang seharusnya begitu
- Yang penting adalah mengambil kode dari URL
- Halaman error localhost bisa ditutup setelah kode di-copy

## Setelah Autentikasi Berhasil
1. Aplikasi akan refresh otomatis
2. Anda akan bisa melihat form upload file
3. File yang diupload akan otomatis dikonversi dan disimpan di Google Drive
4. Link sharing akan dibuat otomatis dengan akses "Anyone with the link"

## Bantuan
Jika mengalami kesulitan atau error yang tidak tercantum di panduan ini, silakan:
1. Coba logout dari Google Account dan login kembali
2. Hapus file token.pickle (jika ada) dan coba proses autentikasi dari awal
3. Pastikan menggunakan versi browser terbaru
