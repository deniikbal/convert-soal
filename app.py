import streamlit as st
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.oxml.shared import qn
from docx.enum.text import WD_COLOR_INDEX
import pandas as pd
import os
from google_drive_helper import upload_to_drive, get_google_auth

# Antarmuka Streamlit
st.title('Aplikasi Format Soal')
st.markdown("""
Upload file Word yang berisi soal-soal untuk diformat ke dalam template tabel.
File akan otomatis dikonversi dan diupload ke Google Docs.
""")

# Cek status autentikasi Google Drive
creds = get_google_auth()
if not creds:
    st.info("Silahkan selesaikan proses autentikasi Google Drive terlebih dahulu")
    st.stop()

# Fungsi untuk memproses file input
def process_input_file(input_file):
    # Baca file Word
    doc = Document(input_file)
    
    # Ekstrak data soal
    questions = []
    current_question = {}
    question_patterns = ('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')
    option_patterns = ('A.', 'B.', 'C.', 'D.', 'E.')
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        # Deteksi nomor soal
        if any(text.startswith(p) for p in question_patterns):
            if current_question:
                # Validasi soal lengkap sebelum ditambahkan
                if all(key in current_question for key in ['number', 'question', 'options', 'answer']):
                    questions.append(current_question)
                else:
                    st.warning(f"Soal {current_question.get('number', '')} tidak lengkap dan akan diabaikan")
            
            # Mulai soal baru
            parts = text.split('.', 1)
            if len(parts) > 1:
                current_question = {
                    'number': parts[0].strip(),
                    'question': parts[1].strip(),
                    'options': [],
                    'answer': ''
                }
        
        # Deteksi pilihan jawaban
        elif any(text.startswith(p) for p in option_patterns):
            if current_question:
                current_question['options'].append(text)
        
        # Deteksi kunci jawaban
        elif text.lower().replace(' ', '').startswith(('kunci:', 'jawaban:')):
            if current_question:
                parts = text.split(':', 1)
                if len(parts) > 1:
                    current_question['answer'] = parts[1].strip()
    
    # Tambahkan soal terakhir jika valid
    if current_question and all(key in current_question for key in ['number', 'question', 'options', 'answer']):
        questions.append(current_question)
    
    # Validasi minimal 1 soal
    if not questions:
        st.error('Format file tidak sesuai. Pastikan file berisi:')
        st.markdown("""
        - Nomor soal (contoh: 1. Pertanyaan...)
        - Pilihan jawaban (contoh: A. Jawaban A)
        - Kunci jawaban (contoh: Kunci: A)
        """)
    
    return questions

# Fungsi untuk membuat template output
def create_template(questions):
    # Buat dokumen baru
    doc = Document()
    
    # Iterasi untuk setiap soal
    for i, question in enumerate(questions):
        # Tambahkan jarak antar tabel jika bukan soal pertama
        if i > 0:
            doc.add_paragraph()  # Tambah baris kosong antara tabel
        
        # Buat tabel 2 kolom x 10 baris
        table = doc.add_table(rows=10, cols=2)
        
        # Set lebar kolom pertama ke 1.5 cm
        for row in table.rows:
            row.cells[0].width = Cm(1.5)
            
        # Isi template sesuai format baru
        table.cell(0, 0).text = 'TS'
        table.cell(0, 1).text = 'PG'
        table.cell(1, 0).text = 'KD'
        table.cell(1, 1).text = ''  # Nomor soal dihapus dari kolom 2 baris 2
        table.cell(2, 0).text = 'KJ'
        table.cell(2, 1).text = question['answer']
        table.cell(3, 0).text = 'ABS'
        table.cell(3, 1).text = ''  # Kolom 2 baris 2 dikosongkan
        
        # Baris 5: Nomor soal dan teks soal
        table.cell(4, 0).text = question['number']
        table.cell(4, 1).text = question['question']
        
        # Baris 6-10: Pilihan jawaban
        for j, option in enumerate(question['options']):
            # Hapus prefix A., B., C., D., E. dari teks option
            option_text = option.split('.', 1)[1].strip() if '.' in option else option
            table.cell(5 + j, 0).text = ['A', 'B', 'C', 'D', 'E'][j]
            table.cell(5 + j, 1).text = option_text
            
        # Format tabel dengan styling
        table.style = 'Table Grid'  # Tambahkan border ke seluruh tabel
        
        for row in table.rows:
            for cell in row.cells:
                # Set alignment ke kiri
                cell.paragraphs[0].alignment = 0  # Left alignment
    
    return doc

# Upload file interface
uploaded_file = st.file_uploader("Upload file soal", type=['docx'])

if uploaded_file is not None:
    output_path = 'output.docx'
    try:
        questions = process_input_file(uploaded_file)
        
        if not questions:
            st.error('File tidak berisi soal yang valid. Pastikan format sesuai!')
        else:
            output_doc = create_template(questions)
            output_doc.save(output_path)
            
            with st.spinner('Mengupload file ke Google Drive...'):
                try:
                    drive_link = upload_to_drive(output_path)
                    st.success('File berhasil diproses dan diupload ke Google Drive!')
                    st.markdown(f'[Buka file di Google Docs]({drive_link})')
                except Exception as e:
                    st.error(f'Error saat upload ke Google Drive: {str(e)}')
                    # Tetap tampilkan opsi download lokal jika upload gagal
                    with open(output_path, "rb") as file:
                        btn = st.download_button(
                            label="Download file output",
                            data=file,
                            file_name="output.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    
    except Exception as e:
        st.error(f'Terjadi error: {str(e)}')

# Tampilkan panduan format file
with st.expander("Format File Input"):
    st.markdown("""
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
    ...
    ```
    """)
