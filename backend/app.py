import os
import json
import uuid
from datetime import datetime

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import save_to_database, get_status, get_reports, update_status
from storage import upload_file, make_public_url
from ocr import extract_info
from svm import sentiment_classification, category_classification

RESPONSES = "./data/chatbot/response.json"
CONTACTS = "./data/chatbot/contact.json"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
    ktp_blob: str
    bukti_blob: str

class StatusData(BaseModel):
    ticket: str
    new_status: str

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def generate_ticket_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = uuid.uuid4().hex[:5].upper()
    return f"TCK-{timestamp}-{random_str}"

@app.post("/extract_info")
async def extract_info_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    nik, nama, gender = extract_info(contents)
    return {"nik": nik, "nama": nama, "gender": gender}

@app.post("/upload_image")
async def upload_image_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    extension = os.path.splitext(file.filename)[1]
    random_str = uuid.uuid4().hex[:12]
    blob_name = upload_file(contents, f"img_{random_str}{extension}")
    public_url = make_public_url(blob_name)
    return {"public_url": public_url}

@app.post("/chat")
async def chat_endpoint(data: UserMessage):
    category = category_classification(data.message)
    sentiment = sentiment_classification(data.message)
    contacts = load_json(CONTACTS)
    responses = load_json(RESPONSES)
    contact = contacts.get(category, "pusat")
    res = responses[category][sentiment]["respon"]
    response = res.replace("{kontak}", contact)
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
        "ktp_blob": data.ktp_blob,
        "bukti_blob": data.bukti_blob,
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
