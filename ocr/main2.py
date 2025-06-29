import pdf2image
import pytesseract
import cv2
import re
import json
import numpy as np
from docx import Document
from pix2tex.cli import LatexOCR

__file__="material/Module 5 Memory Management.pptx.pdf"
current_dir=os.getcwd()
file_path=os.path.join(current_dir, __file__)
print(file_path)

def clean_text(text):
    """Comprehensive text cleaning with word boundary reconstruction"""
    # Step 1: Fix specific OCR artifacts
    text = re.sub(r'(\b)e([A-Z])', r'\1\2', text)  # Remove stray 'e' before capitals
    text = re.sub(r'\b(\d+);\b', r'\1', text)      # Remove semicolons after numbers
    
    # Step 2: Reconstruct word boundaries
    # Case transitions (lower to upper)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Case transitions (upper to upper) when followed by lowercase
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', text)
    # Digit-letter transitions
    text = re.sub(r'([0-9])([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])([0-9])', r'\1 \2', text)
    
    # Step 3: Standard cleaning
    text = re.sub(r'[^\w\s\.\-\+\*/\^\(\)\[\]\{\}=,;:&@#%$]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s([\.\,\;:])', r'\1', text)
    text = re.sub(r'\bpage\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
    
    # Step 4: Fix common OCR errors in words
    replacements = {
        r'\boperatingsystem\b': 'operating system',
        r'\baddressspace\b': 'address space',
        r'\bmultitasking\b': 'multi-tasking',
        r'\bmainmemory\b': 'main memory',
        r'\bcpubound\b': 'CPU-bound',
        r'\biobound\b': 'I/O-bound'
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text.strip()

def extract_pdf_content(pdf_path):
    text_content = ""
    img = LatexOCR()  
    
    images = pdf2image.convert_from_path(pdf_path)
    
    for i, image in enumerate(images):
        # Preprocess image
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Detect equations (connected components analysis)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        #get text
        page_text = pytesseract.image_to_string(gray)
        text_content += page_text + "\n\n"
        
       #handling equations
        equation_bboxes = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 20 < w < 500 and 20 < h < 100:  
                equation_img = gray[y:y+h, x:x+w]
                try:
                    equation = img(Image.fromarray(equation_img))
                    text_content += f"\nEQUATION: {equation}\n"
                except:
                    pass
                equation_bboxes.append((x, y, w, h))
    
    return text_content


cleaned_content = extract_pdf_content(file_path)
with open("cleaned_content.txt", "w") as f:
    f.write(cleaned_content)