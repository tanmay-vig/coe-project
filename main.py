# only run this file, none of the other files
# This script serves as the main entry point for the Question Generator Tool.

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Pytesseract.ocr import run_ocr_interface as extract_with_ocr
from Langchain.pdf_img_loader import load_pdf as extract_with_langchain
from questions_generation.question_gen import run_question_generation as generate_questions
from Store_and_embed.ollama_store import load_questions as embed_questions
from Store_and_embed.ollama_search import search_questions 

def main():
    print("📘 Welcome to the Question Generator Tool!")

    # # Step 1: Extraction Method
    # # Comment out if not needed
    # method = input("Choose extraction method [ocr/langchain]: ").strip().lower()

    # if method == "ocr":
    #     text = extract_with_ocr()
    # elif method == "langchain":
    #     text = extract_with_langchain()
    # else:
    #     print("❌ Invalid method. Please choose 'ocr' or 'langchain'.")
    #     return
    
    # # Comment out if not needed
    # # Step 3: Generate Questions
    # generate_questions()

    # # Comment out if not needed
    # # Step 4: Create Embeddings and Store in FAISS
    # embed_questions()

    # Step 5: Take Query and Filters
    print("\nReady to search your generated questions!")
    query = input("🔸 Enter your query: ").strip()
    try:
        marks = int(input("📝 Desired marks (1/2/3/5): ").strip())
    except ValueError:
        print("❌ Invalid number for marks.")
        return
    difficulty = input("📈 Difficulty level (Easy/Medium/Hard/Challenging/Moderate/Medium-Hard): ").strip()
    cognitive = input("🧠 Cognitive level (Remembering/Applying/Creating/Analyzing/Evaluating/Understanding ...): ").strip()
    # Step 6: Perform Search
    search_questions(
        query=query if query else None,
        marks=marks if marks in [1, 2, 3, 5] else None,
        difficulty=difficulty if difficulty else None,
        cognitive_level=cognitive if cognitive else None
    )

if __name__ == "__main__":
    main()
