import os
import fitz  # PyMuPDF
import pytesseract
import cv2
import numpy as np
from PIL import Image

DATASET_DIR = "dataset"
OUTPUT_PATH = "output/extracted_output.txt"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def extract_text_from_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    return pytesseract.image_to_string(gray)

def extract_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = extract_text_from_image(img)
        full_text.append(text)
    return "\n".join(full_text)

def process_dataset():
    os.makedirs("output", exist_ok=True)
    combined_text = ""

    for file in os.listdir(DATASET_DIR):
        path = os.path.join(DATASET_DIR, file)
        if file.lower().endswith(".pdf"):
            print(f"📄 Processing PDF: {file}")
            combined_text += extract_from_pdf(path) + "\n\n"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(combined_text)

    print(f"✅ OCR completed. Output saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    process_dataset()
