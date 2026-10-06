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
MIN_TEXT_CHARS = 50

ALLOWED_FILE_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff"]
DESTINATION_URL = "Placeholder for where we send the file post OCR"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_MB * 1024 * 1024

ocr = PaddleOCR(
    lang='en',
    use_doc_orientation_classify=False,
    use_text_detection=True,
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

def render_pdf_as_image(page: fitz.Page) -> np.ndarray:
    pixmap = page.get_pixmap(dpi=PDF_DPI)
    img = np.frombuffer(pixmap.samples, np.uint8).reshape(pixmap.height, pixmap.width, pixmap.n)
    if pixmap.n == 4:
        img = img[:, :, :3]
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

#PROCESSING WORKFLOW
def process_file(data: bytes, filename:str) -> dict: #uses ocr pipeline to process an uploaded image or pdf
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_FILE_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    page_texts, all_scores = [], []

    if ext == ".pdf":
        doc = fitz.open(stream=data, filetype="pdf")
        if len(doc) > MAX_PAGES:
            raise ValueError(f"PDF has {len(doc)} pages (max {MAX_PAGES})")
        for page in doc:
            text = page.get_text().strip()
            if len(text) >= MIN_TEXT_CHARS:      # digital PDF, no OCR needed
                page_texts.append(text)
                continue
            text, scores = process_image(render_pdf_as_image(page))
            page_texts.append(text)
            all_scores.extend(scores)
    else:
        img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image")
        text, scores = process_image(img)
        page_texts.append(text)
        all_scores.extend(scores)

    return {
        "text": "\n\n".join(page_texts),
        "page_count": len(page_texts),
        "avg_confidence": sum(all_scores) / len(all_scores) if all_scores else None,
    }
