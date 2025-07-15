# app/services/ocr_utils.py

import pytesseract
import cv2
import fitz  # PyMuPDF
import os
import re
from PIL import Image
import numpy as np
import io

# === Core OCR + Refinement ===

def extract_text_from_pdf(file):
    """
    Extract text from both text-based and scanned PDFs from a FastAPI UploadFile object.
    Handles both text-based pages and image-based OCR fallbacks.
    """
    try:
        file_bytes = file.file.read()  # ✅ Read actual content
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""

        for page in doc:
            text = page.get_text()
            if text.strip():
                full_text += text
            else:
                # Fallback to OCR if page has no selectable text
                pix = page.get_pixmap(dpi=300)
                img_bytes = pix.tobytes("png")
                img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
                text = pytesseract.image_to_string(img)
                full_text += text

        doc.close()
        return refine_text(full_text)
    except Exception as e:
        return f"OCR failed: {str(e)}"


def refine_text(raw_text):
    """Clean OCR text, allow math symbols and remove junk."""
    text = raw_text.replace('\n', ' ').strip()
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # remove non-ASCII
    text = re.sub(r'\s+', ' ', text)
    return text

# === Math Symbol / Diagram Detection ===

def analyze_text(text):
    """Detect whether text contains math expressions or diagrams."""
    math_keywords = ['∫', '∑', '∂', '=', '≠', '≤', '≥', '+', '-', '*', '/', '^', '√']
    diagram_keywords = ['figure', 'diagram', 'shown below', 'label', 'draw']

    is_math = any(sym in text for sym in math_keywords)
    has_diagram = any(kw.lower() in text.lower() for kw in diagram_keywords)

    return {
        "is_math": is_math,
        "has_diagram": has_diagram
    }

# === Image OCR handler ===

def handle_image(image_path):
    """Handle standalone image OCR."""
    try:
        img = cv2.imread(image_path)
        text = pytesseract.image_to_string(img)
        analysis = analyze_text(text)
        return {
            "text": refine_text(text),
            "analysis": analysis
        }
    except Exception as e:
        return {
            "error": str(e),
            "text": "",
            "analysis": {}
        }

# === Diagram detection via contours ===

def detect_contours(image_path):
    """Detect diagram-like contours in an image."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Heuristic: return True if multiple large contours
    diagram_like = [c for c in contours if cv2.contourArea(c) > 500]
    return len(diagram_like) >= 2

def detect_images_in_page(page):
    """Detect if a PyMuPDF page contains images."""
    return len(page.get_images(full=True)) > 0

# === Optional: LangChain-Compatible Loader ===

from langchain_community.document_loaders import PyPDFLoader
from unstructured.partition.pdf import partition_pdf

def extract_text_fallback(path):
    """Fallback OCR if PyPDFLoader fails."""
    elements = partition_pdf(filename=path, strategy="hi_res")
    texts = []
    for element in elements:
        try:
            img = Image.fromarray(element.to_image())
            text = pytesseract.image_to_string(img)
            texts.append(text)
        except Exception:
            continue
    return "\n".join(texts)

def smart_pdf_loader(path):
    """Try structured loading; fallback to OCR."""
    try:
        loader = PyPDFLoader(path)
        return loader.load()
    except Exception:
        print("[!] Falling back to OCR...")
        return [{"page_content": extract_text_fallback(path)}]
