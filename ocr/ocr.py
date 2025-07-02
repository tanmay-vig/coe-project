from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe"  


image_path = "medi.png"
image = Image.open(image_path)

text = pytesseract.image_to_string(image)

print("Extracted Text:")
print(text)
