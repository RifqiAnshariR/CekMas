import os
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

BUCKET_NAME = "public-uploads-bucket"

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

def upload_file(contents: bytes, blob_name: str):
    blob = bucket.blob(blob_name)
    blob.upload_from_string(contents)
    return blob_name

def make_public_url(blob_name: str):
    blob = bucket.blob(blob_name)
    blob.make_public()
    return blob.public_url

def delete_file(blob_name: str):
    blob = bucket.blob(blob_name)
    blob.delete()
