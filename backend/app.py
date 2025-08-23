import os
import json
import random
import string
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import save_to_database, get_status, get_reports, update_status
from ocr import extract_info
from svm import sentiment_classification, category_classification

UPLOAD_DIR = "./uploads"
RESPONSES = "./data/chatbot/response.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    message: str

class UserData(BaseModel):
    nik: str
    name: str
    gender: str

class ReportData(BaseModel):
    email: str
    nik: str
    name: str
    location: str
    category: str
    message: str
    sentiment: str

class StatusData(BaseModel):
    ticket: str
    new_status: str

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def generate_ticket_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TCK-{timestamp}-{rand_str}"

@app.post("/upload_ktp")
async def upload_ktp_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    nik, nama, gender = extract_info(contents)
    return {"nik": nik, "nama": nama, "gender": gender}

@app.post("/upload_bukti")
async def upload_bukti_endpoint(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename, "saved_to": file_path}

@app.post("/chat")
async def chat_endpoint(data: UserMessage):
    category = category_classification(data.message)
    sentiment = sentiment_classification(data.message)
    responses = load_json(RESPONSES)
    response = responses[category][sentiment]["respon"]
    follow_up_1 = responses[category][sentiment]["follow_up_1"]
    follow_up_2 = responses[category][sentiment]["follow_up_2"]
    return {
        "response": response,
        "follow_up_1": follow_up_1,
        "follow_up_2": follow_up_2,
        "category": category,
        "sentiment": sentiment
    }

@app.post("/save_report")
async def save_report_endpoint(data: ReportData):
    ticket = generate_ticket_id()
    row = {
        "ticket": ticket,
        "email": data.email,
        "nik": data.nik,
        "name": data.name,
        "location": data.location,
        "category": data.category,
        "message": data.message,
        "sentiment": data.sentiment,
        "time": datetime.now(),
        "status": "Belum selesai"
    }
    save_to_database(row)
    return {"ticket": ticket}

@app.get("/status/{ticket}")
async def get_status_endpoint(ticket: str):
    data = get_status(ticket)
    if not data:
        return {"status": None, "email": "", "nik": "", "name": ""}
    return {
        "email": data["email"],
        "nik": data["nik"],
        "name": data["name"],
        "status": data["status"]
    }

# Admin
@app.get("/admin/reports")
async def get_reports_endpoint():
    rows = get_reports()
    return {"reports": rows}

@app.patch("/admin/update_status")
async def update_status_endpoint(data: StatusData):
    update_status(data.ticket, data.new_status)
    return {"ticket": data.ticket, "status": data.new_status}
