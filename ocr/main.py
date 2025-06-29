from langchain_community.document_loaders import UnstructuredFileLoader, PyPDFLoader
from langchain_community.document_loaders.image import UnstructuredImageLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import re
import pytesseract
from pdf2image import convert_from_path
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from typing import List, Tuple, Dict, Any

__file__="material/Module 5 Memory Management.pptx.pdf"
current_dir=os.getcwd()
file_path=os.path.join(current_dir, __file__)
print(file_path)

images = convert_from_path(file_path, dpi=500)
docs = []
for i, image in enumerate(images):
        image_path = f"temp_page_{i}.png"
        image.save(image_path, "PNG")
        
        
        loader = UnstructuredImageLoader(image_path, strategy="ocr_only", ocr_languages="eng")
        page_docs = loader.load()
        

        for doc in page_docs:
            doc.metadata["page"] = i + 1
            doc.metadata["source"] = file_path
        
        docs.extend(page_docs)
        os.remove(image_path)

print(len(docs[0].page_content))
# print(docs)


for doc in docs:
        text = doc.page_content
        
        # 1. Remove headers/footers
        text = re.sub(r'^.*\n\d{1,3}\n', '', text, flags=re.MULTILINE)
        
        # 2. Fix hyphenated words
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
        
        # 3. Fix common OCR errors
        # text = re.sub(r'(\d)\s*[oO]\s*(\d)', r'\10\2', text)  # 1o0 → 100
        text = re.sub(r'[|lI]\s*[\'’]\s*([a-zA-Z])', r"I'\1", text)  # I ' m → I'm
        
        # 4. Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        doc.page_content = text
text=""
for i in docs:
       text += i.page_content + "\n\n"
with open("cleaned_content.txt", "w") as f:
    f.write(text)