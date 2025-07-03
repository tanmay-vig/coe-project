import fitz  # PyMuPDF
from langchain.schema import Document

def load_pdf_to_docs(pdf_path):
    """
    Extracts text (including math symbols where possible) from a PDF
    and returns a list of LangChain Document objects.
    """
    doc = fitz.open(pdf_path)
    docs = []

    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():  # skip empty pages
            docs.append(Document(
                page_content=text,
                metadata={
                    "source": pdf_path,
                    "page": i + 1
                }
            ))
    return docs

def save_docs_to_txt(docs, output_path="output.txt"):
    """
    Saves list of Document objects to a .txt file with page headers.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for doc in docs:
            f.write(f"\n--- Page {doc.metadata['page']} ---\n")
            f.write(doc.page_content.strip())
            f.write("\n")
    print(f"✅ Saved {len(docs)} pages to {output_path}")
    
def load_pdf():
    pdf_path = input("Enter the path to the PDF file or image: ").strip()
    docs = load_pdf_to_docs(pdf_path)
    save_docs_to_txt(docs, "extracted_text.txt")
    print(f"Extracted {len(docs)} pages from {pdf_path}.")
    print(docs[0].page_content[:500])  # preview first page
    return docs

if __name__ == "__main__":
    # Example usage:
    # pdf_path = "C:\\Users\\hp\\projects\\Question_Generator\\Data_Preprocessing\\upload\\pdf1.pdf"
    # pdf_path = "C:\\Users\\hp\\projects\\Question_Generator\\Data_Preprocessing\\upload\\pdf2.pdf"
    pdf_path = input("Enter the path to the PDF file or image: ").strip()
    docs = load_pdf_to_docs(pdf_path)
    save_docs_to_txt(docs, "extracted_text.txt")

    # Now `docs` can be directly used for embedding
    print(f"Extracted {len(docs)} pages.")
    print(docs[0].page_content[:500])  # preview first page
