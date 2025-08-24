import sqlite3

DB_PATH = './db/laporan.db'

def save_to_database(data):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO laporan (tiket, email, nik, nama, lokasi, kategori, pesan, sentimen, waktu, ktp_blob, bukti_blob, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('ticket'),
            data.get('email'),
            data.get('nik'),
            data.get('name'),
            data.get('location'),
            data.get('category'),
            data.get('message'),
            data.get('sentiment'),
            data.get('time'),
            data.get('ktp_blob'),
            data.get('bukti_blob'),
            data.get('status')
        ))

def get_status(ticket):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT email, nik, nama, status FROM laporan WHERE tiket = ?", (ticket,))
        row = c.fetchone()
        if row:
            return {"email": row[0], "nik": row[1], "name": row[2], "status": row[3]}
        return None

def get_reports():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM laporan")
        rows = c.fetchall()
        reports = []
        for row in rows:
            reports.append({
                "ticket": row[1],
                "email": row[2],
                "nik": row[3],
                "nama": row[4],
                "lokasi": row[5],
                "kategori": row[6],
                "pesan": row[7],
                "sentimen": row[8],
                "waktu": row[9],
                "ktp_blob": row[10],
                "bukti_blob": row[11],
                "status": row[12]
            })
        return reports

def update_status(ticket, new_status):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("UPDATE laporan SET status = ? WHERE tiket = ?", (new_status, ticket))
