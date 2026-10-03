import os
import threading
import cv2
import numpy as np
import requests
from flask import Flask, request, jsonify, render_template
from paddleocr import PaddleOCR

#CONFIG
MAX_UPLOAD_MB = 20
MAX_PAGES = 10
PDF_DPI = 300

ALLOWED_FILE_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff"]
DESTINATION_URL = "Placeholder for where we send the file post OCR"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_MB * 1024 * 1024

ocr = PaddleOCR(
    lang='en',
    use_doc_orientation_classify=False,
    use_text_detection=False,
    use_textline_orientation=False
)

ocr_lock = threading.Lock()

#OCR
def process_image(image: np.ndarray) -> tuple[str, list[float]]:
    with ocr_lock:
        results = ocr.predict(image)
    lines, scores = [], []
    for page in results:
        lines.append(page["text"])
        scores.append(page["confidence score"])
    return "\n".join(lines), scores

def render_pdf_as_image(page: "fitz.Page") -> np.ndarray:
    pixmap = page.get_pixmap(dpi=PDF_DPI)
    img = np.frombuffer(pixmap.samples, np.uint8).reshape(pixmap.height, pixmap.width, pixmap.n)
    if pixmap.n == 4:
        img = img[:, :, :3]
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

#PROCESSING WORKFLOW
def process_file(data: bytes, filename:str) -> dict: #uses ocr pipeline to process an uploaded image or pdf
    pass

def send_output(result: dict):
    pass

#ROUTES
@app.route("/upload", methods=["POST"])
def upload(): #This is the function the app would call when processing an uploaded image
    pass