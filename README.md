# CekMas (Cek Masalah): Aplikasi Pelaporan Publik Berbasis AI

## MVP
- **Verifikasi Identitas Otomatis**: OCR KTP untuk ekstraksi NIK, nama, dan jenis kelamin.  
- **Formulir & Chat Interaktif**: Input laporan, upload bukti, serta respon AI otomatis.  
- **Analisis AI**: Klasifikasi kategori laporan & analisis sentimen menggunakan SVM.  
- **Penyimpanan Aman**: Data laporan, KTP, dan bukti tersimpan di SQL & Google Cloud Storage (Blob).  
- **Dashboard Admin**: Login, pantau laporan, update status real-time.  
- **Tiket Laporan**: Nomor unik untuk tracking status laporan.  

## Arsitektur
- **Frontend**: HTML, CSS, JavaScript (UI minimalis: User & Admin).  
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
  - Buat storage GCS dan download file key.json.
  - Buat file .env berisi path ke key.json dan simpan dalam GOOGLE_APPLICATION_CREDENTIALS.
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
- Upload KTP  
- Isi formulir laporan. Beberapa sudah terisi otomatis.  
- Chat keluhan & upload bukti (opsional)  
- Mendapat tiket laporan untuk tracking  

**Admin**  
- Login ke dashboard  
- Memantau daftar laporan  
- Update status dari "Belum Selesai" ke "Selesai"  
- Kirim konfirmasi ke user via email (manual)  