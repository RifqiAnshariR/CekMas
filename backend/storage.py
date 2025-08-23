from google.cloud import storage

# Init client
client = storage.Client()

# 1. Create bucket
bucket_name = "my-unique-bucket-name-123"
bucket = client.bucket(bucket_name)
bucket.location = "US"  # bisa diganti sesuai kebutuhan
bucket = client.create_bucket(bucket)
print(f"Bucket {bucket_name} created.")

# 2. Upload file (optional)
blob = bucket.blob("example.txt")
blob.upload_from_string("Hello GCS!")
print("File uploaded.")

# 3. Delete file (optional)
blob.delete()
print("File deleted.")

# 4. Delete bucket
bucket.delete()
print(f"Bucket {bucket_name} deleted.")
