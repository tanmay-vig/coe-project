import fitz  
import pytesseract
from PIL import Image
import io


pdf_path = 'medic.pdf'


pdf_document = fitz.open(pdf_path)


for page_number in range(len(pdf_document)):
    page = pdf_document.load_page(page_number)
    pix = page.get_pixmap()  
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))

    
    text = pytesseract.image_to_string(img)
    print(f"\n--- Text from page {page_number+1} ---\n")
    print(text)

pdf_document.close()
