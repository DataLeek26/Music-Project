"""TEMPORARY CODE WRITTEN BY AI (CLAUDE) TO TEST THE AZURE PIPELINE"""

# worker.py
import os, json, time, logging
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient
from azure.storage.blob import BlobClient
from ocr import process_file   # importing this loads PaddleOCR once

logging.basicConfig(level=logging.INFO)
cred = DefaultAzureCredential()
ACCOUNT = os.environ["STORAGE_ACCOUNT"]

queue = QueueClient(
    f"https://{ACCOUNT}.queue.core.windows.net",
    os.environ.get("QUEUE_NAME", "ocr-jobs"),
    credential=cred,
)

def send_output(job: dict, result: dict):
    # Replaces DESTINATION_URL. Later: send result["text"] to Azure OpenAI,
    # validate the JSON, insert into SQL, and mark the job completed.
    logging.info("job %s: %d pages, %d chars, confidence %s",
                 job["job_id"], result["page_count"],
                 len(result["text"]), result["avg_confidence"])

def handle(job: dict):
    blob = BlobClient(
        f"https://{ACCOUNT}.blob.core.windows.net",
        container_name="uploads",
        blob_name=job["blob_name"],
        credential=cred,
    )
    data = blob.download_blob().readall()
    result = process_file(data, job["blob_name"])
    send_output(job, result)

while True:
    got_any = False
    for msg in queue.receive_messages(visibility_timeout=600, max_messages=1):
        got_any = True
        job = json.loads(msg.content)
        try:
            handle(job)
            queue.delete_message(msg)
        except Exception:
            logging.exception("job %s failed", job.get("job_id"))
            if msg.dequeue_count >= 3:
                queue.delete_message(msg)   # later: mark job failed in SQL
    if not got_any:
        time.sleep(5)