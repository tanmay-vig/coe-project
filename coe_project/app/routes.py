from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.ocr_utils import extract_text_from_pdf
from app.services.class_structure import parse_structure
from app.services.preprocessing import clean_text
from app.services.question_gen import process_text_to_questions
from app.services.subtopic_cleaner import clean_subtopics
from app.services.embedding_store import load_questions, store_in_faiss
from app.services.chat import get_conversational_chain
from app.services.search_engine import search_questions
from app.config import FAISS_INDEX_PATH

router = APIRouter()
chat_chain = get_conversational_chain()

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    # ✅ Check if file was uploaded
    if not file:
        raise HTTPException(status_code=400, detail="❌ No file uploaded.")

    # Step 1: OCR
    extracted_text = extract_text_from_pdf(file)

    # Step 2: Structure detection
    structure = parse_structure(extracted_text)

    # Step 3: Preprocess
    cleaned_text = clean_text(extracted_text)
    print("🧹 Cleaned Text Preview:", cleaned_text[:500])

    # Step 4: Generate questions
    generated_questions = process_text_to_questions(cleaned_text)

    # Step 5: Subtopic cleaning
    questions_with_subtopics = clean_subtopics(generated_questions)

    # ✅ Step 6: Store in FAISS using correct path to output_questions.json
    store_in_faiss(
        load_questions("app/data/sample_pdfs/output_questions.json"),  # ✅ corrected path
        index_path=str(FAISS_INDEX_PATH)
    )

    return {
        "message": "✅ PDF processed and indexed successfully.",
        "structure": structure,
        "questions_generated": len(generated_questions)
    }


@router.post("/chat/")
async def chat_with_bot(message: str):
    response = chat_chain.run(message)
    return {"response": response}


@router.get("/search/")
async def semantic_search(query: str):
    results = search_questions(query)
    return JSONResponse(content=results)
