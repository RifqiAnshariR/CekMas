import os
from dotenv import load_dotenv
from google.cloud import storage
from PIL import Image

load_dotenv()
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

BUCKET_NAME = "public-uploads-bucket"

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

def upload_file(contents: bytes, bucket_name: str, blob_name: str):
    blob = bucket.blob(blob_name)
    blob.upload_from_string(contents)
    return bucket_name, blob_name

def download_file(blob_name: str, image_path: str):
    blob = bucket.blob(blob_name)
    blob.download_to_filename(image_path)
    return image_path

def delete_file(blob_name: str):
    blob = bucket.blob(blob_name)
    blob.delete()
