from google.cloud import storage
from google.api_core.exceptions import Forbidden, NotFound
from fastapi import FastAPI
import os


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello from Cloud Run!",
        "environment": os.getenv("APP_ENV", "development")
    }


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/private-file")
def read_private_file():
    bucket_name = os.getenv("GCS_BUCKET", "test-bucket-akshay")
    object_name = os.getenv("GCS_OBJECT", "Hello.txt")

    try:
        client = storage.Client()
        blob = client.bucket(bucket_name).blob(object_name)
        content = blob.download_as_text()

        return {
            "bucket": bucket_name,
            "object": object_name,
            "content": content
        }

    except Forbidden:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Check the runtime service account's bucket access."
        )

    except NotFound:
        raise HTTPException(
            status_code=404,
            detail="The requested bucket object was not found."
        )
