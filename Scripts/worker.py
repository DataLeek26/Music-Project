"""TEMPORARY CODE WRITTEN BY AI (CLAUDE) TO TEST THE AZURE PIPELINE"""

import os, json, tempfile, logging
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient
from azure.storage.blob import BlobClient
from ocr import pdf_to_text   # PaddleOCR is loaded once at import time

logging.basicConfig(level=logging.INFO)
cred = DefaultAzureCredential()

ACCOUNT = os.environ["STORAGE_ACCOUNT"]
queue = QueueClient(f"https://{ACCOUNT}.queue.core.windows.net",
                    os.environ.get("QUEUE_NAME", "ocr-jobs"), credential=cred)

def process(job):
    blob = BlobClient(f"https://{ACCOUNT}.blob.core.windows.net",
                      container_name="uploads", blob_name=job["blob_name"],
                      credential=cred)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(blob.download_blob().readall()); f.flush()
        text = pdf_to_text(f.name)
    # TODO: call Azure OpenAI -> validate JSON -> insert into SQL -> mark job completed
    logging.info("job %s: %d chars extracted", job["job_id"], len(text))

while True:
    got_any = False
    for msg in queue.receive_messages(visibility_timeout=600, max_messages=1):
        got_any = True
        job = json.loads(msg.content)   # note: queue messages may be base64-encoded depending on how they were sent
        try:
            process(job)
            queue.delete_message(msg)
        except Exception:
            logging.exception("job failed")
            if msg.dequeue_count >= 3:
                # mark job failed in SQL, then drop it so it doesn't loop forever
                queue.delete_message(msg)
    if not got_any:
        import time; time.sleep(5)