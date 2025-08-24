import os
from dotenv import load_dotenv
import sqlite3
from google.cloud import storage

load_dotenv()
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

BUCKET_NAME = "public-uploads-bucket"
REGION = "ASIA-SOUTHEAST1"      # Singapore
DB_NAME = "./backend/db/laporan.db"

client = storage.Client()

def init_storage(bucket_name: str, location: str):
    bucket = client.bucket(bucket_name)
    bucket.location = location
    bucket = client.create_bucket(bucket)
    bucket.add_lifecycle_delete_rule(age=30)        # 30 days period
    bucket.patch()

def init_db(db_name: str):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS laporan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tiket VARCHAR,
            email TEXT,
            nik INTEGER,
            nama TEXT,
            lokasi TEXT,
            kategori TEXT,
            pesan TEXT,
            sentimen TEXT,
            waktu TIMESTAMP,
            ktp_blob TEXT,
            bukti_blob TEXT,
            status TEXT
        );
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_storage(BUCKET_NAME, REGION)
    init_db(DB_NAME)
