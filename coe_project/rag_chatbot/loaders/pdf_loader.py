# loaders/pdf_loader.py

from langchain.document_loaders import PyPDFLoader
from unstructured.partition.pdf import partition_pdf
from PIL import Image
import pytesseract

def extract_text_fallback(path):
    elements = partition_pdf(filename=path, strategy="hi_res")
    texts = []
    for element in elements:
        try:
            img = Image.fromarray(element.to_image())
            text = pytesseract.image_to_string(img)
            texts.append(text)
        except Exception as e:
            continue
    return "\n".join(texts)

def smart_pdf_loader(path):
    try:
        loader = PyPDFLoader(path)
        return loader.load()
    except Exception:
        print("[!] Falling back to OCR...")
        return [{"page_content": extract_text_fallback(path)}]
