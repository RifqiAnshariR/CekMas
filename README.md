# CekMas (Cek Masalah): Aplikasi Pelaporan Publik Berbasis AI

## MVP
- **Verifikasi Identitas Otomatis**: OCR KTP untuk ekstrak NIK, nama, dan jenis kelamin. Fitur *auto fill* formulir identitas.
- **Analisis AI**: Klasifikasi kategori laporan & analisis sentimen menggunakan model SVM.
- **Chat Interaktif**: Respon chat cepat. Chatbot berbasis rule-based.
- **Tiket Laporan**: Nomor unik untuk melacak status laporan.
- **Penyimpanan Aman**: Informasi pelapor serta foto KTP dan bukti tersimpan di SQL dan Google Cloud Storage (Blob). Penyimpanan foto KTP dan bukti disimpan 30 hari.
- **Dashboard Admin**: Login dan pantau laporan juga update status real-time laporan.

## Arsitektur
- **Frontend**: HTML, CSS, JavaScript (UI minimalis: User dan Admin).  
- **Backend**: Python FastAPI.  
- **Database**: SQLite.  
- **Storage**: Google Cloud Storage (Blob).  
- **AI Models**:  
  - OCR untuk ekstraksi data KTP.  
  - SVM untuk klasifikasi laporan & sentimen.  

## Alur Menjalankan Proyek
- Clone repository. Di terminal: 
```bash
git clone https://github.com/RifqiAnshariR/CekMas.git
```
- Setup awal Google Cloud Storage (GCS):
  - Buat storage GCS di [Google Cloud Console](https://console.cloud.google.com/) dan download file kredensial key.json.
  - Buat file .env berisi path ke key.json. 
  ```env
     GOOGLE_APPLICATION_CREDENTIALS=./path/to/key.json
  ```
- Setup awal:
```bash
cd CekMas
python -m venv .venv
pip install -r requirments.txt
python setup.py
```
- Jalankan backend:
```bash
cd backend
uvicorn app:app --reload
```
- Jalankan frontend (pastikan sudah ada live-server):
```bash
cd ../frontend
live-server ./user
live-server ./admin
```

## Alur Operasi
**User**  
- Upload gambar KTP.  
- Isi formulir identitas. Beberapa sudah terisi otomatis.  
- Chat keluhan & upload bukti jika ada.  
- Mendapat tiket laporan untuk melacak status.  

**Admin**  
- Login ke dashboard.  
- Memantau daftar laporan. Dapat update status dari "Belum Selesai" menjadi "Selesai".  
- Kirim konfirmasi atau tindak lanjut ke user via email secara manual.  