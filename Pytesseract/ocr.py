def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_ocr_interface():
    import os
    from refinement import handle_image
    from refinement import handle_pdf

    print("📝 Welcome to the OCR Processor")
    
    # Optional text input
    text_input = input("Enter some text (or press Enter to skip): ").strip()
    if text_input:
        print(f"\nReceived text input: {text_input[:500]}\n")

    # File input
    file_path = input("Enter the path to an image or PDF file: ").strip()

    if not os.path.exists(file_path):
        print("❌ File does not exist.")
        return

    filename = os.path.basename(file_path)

    if not allowed_file(filename):
        print("❌ Unsupported file format.")
        return

    if filename.lower().endswith('.pdf'):
        result = handle_pdf(file_path)
    elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        result = handle_image(file_path)
    else:
        result = "Unsupported file format."

    print("\n📄 Extracted Content:\n")
    
    output_path = "extracted_text.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"\n✅ Output saved to {output_path}")
    print(result)

# Run the interface
if __name__ == '__main__':
    run_ocr_interface()
