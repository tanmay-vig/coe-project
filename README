# 📚 Local AI-Powered PDF Question Generator

An intelligent, local-first system to **analyze academic PDFs**, **extract structured content**, and **generate exam-style questions** using **LLMs via Ollama** — all without needing GPUs or cloud APIs.

---

## 🚀 Project Overview

This project allows educators, students, and curriculum designers to:

- Upload academic PDFs (handwritten/printed)
- Extract structured topics, subtopics, definitions, and examples
- Automatically generate exam-style questions (MCQ, short, descriptive)
- Classify questions under subtopics
- Store embeddings for semantic search using FAISS
- Run entirely **offline** using [Ollama](https://ollama.com/) and local LLMs like `gemma:2b`

---

## 🧠 Tech Stack

| Layer        | Tech |
|--------------|------|
| Backend API  | FastAPI |
| Embedding & RAG | LangChain + Ollama + FAISS |
| OCR Support  | PyMuPDF, Tesseract (via `pytesseract`), OpenCV |
| LLM Models   | `gemma:2b` (via Ollama) |
| File Handling| `PyPDFLoader`, `RecursiveCharacterTextSplitter` |
| Subtopic Classification | Rule-based tagging |
| Dev Tools    | PowerShell/Terminal + VS Code + Docker (optional) |

---

## 📂 Folder Structure

coe_project/
├── app/                              # FastAPI application
│   ├── __pycache__
│   ├── main.py                       # App entrypoint
│   ├── routes.py                     # API routes
│   ├── config.py                     # Configuration
│   ├── dependencies             //empty
│   ├── services/                     # Core logic
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── ocr_utils.py              # PDF/image text extraction
│   │   ├── class_structure.py        # Detects chapters, sections, etc.
│   │   ├── preprocessing.py          # Cleans up raw text
│   │   ├── question_gen.py           # Generates questions using Ollama
│   │   ├── rag_pipeline.py           # LangChain/Ollama RAG logic
│   │   ├── chat.py                   # Handles conversation history
│   │   ├── search_engine.py                   # Handles conversation history
│   │   ├── subtopic_cleaner.py                   # Handles conversation history
│   │   └── embedding_store.py        # FAISS index management
│   ├── utils/
│   │   ├── file_handler.py           # Handles uploads and storage
│   │   └── structure_parser.py       # Custom text parsing logic
│   └── data/
│       ├── faiss_index_ollama/
│       │       ├── index.faiss
│       │       └── index.pkl
│       ├── sample_pdfs/
│       │       ├── extracted_output.txt
│       │       ├── keyword.json
│       │       ├── output_questions.json
│       │       ├── questions.json
│       │       ├── pdf
│       │       └── pdf_extract
│       └── uploads/                 # Uploaded PDFs or images
 |
├── langflow_project/                # Optional: For UI in future
│   └── (Langflow setup here)
├── backend                # empty
│   └── (backend setup here)
 |
├── tests/
│   └── test_pipeline.py  
│
└── requirements.txt


## ⚙️ Features

- ✅ PDF (text or scanned) ingestion
- ✅ OCR fallback using Tesseract for image-based text
- ✅ Structured content extraction (chapters → topics → subtopics)
- ✅ LLM-powered question generation via Ollama
- ✅ MCQ/short/descriptive format support
- ✅ Fast semantic search using FAISS
- ✅ Local-first, private and offline

---

## 📥 How to Run

> **Prerequisites**:
> - Python ≥ 3.10
> - [Ollama](https://ollama.com) with `gemma:2b` model pulled
> - `Tesseract` installed (`sudo apt install tesseract-ocr` on Linux or [Windows installer](https://github.com/tesseract-ocr/tesseract))

---

### 🛠 Setup

```bash
# Clone the repo
git clone https://github.com/your-username/local-question-generator.git
cd local-question-generator

# Setup Python env
conda create -n coeenv python=3.10 -y
conda activate coeenv

# Install dependencies
pip install -r requirements.txt

🧪 Run the Backend
bash
Copy
Edit
# Ensure Ollama is running with gemma:2b
ollama run gemma:2b

# Then in another terminal:
uvicorn app.main:app --reload

📄 Sample API Usage
1. Upload PDF
bash
Copy
Edit
curl -X POST http://127.0.0.1:8000/api/upload/ \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/your/pdf.pdf"
2. Semantic Search
http
Copy
Edit
GET /api/search/?query=what is generative AI?
3. Chat with Content
http
Copy
Edit
POST /api/chat/?message=How does it detect emotion?
📌 Sample Output
json
Copy
Edit
{
  "question": "What is the main problem that MoodMatch AI aims to solve?",
  "subtopic": "Innovation Scope",
  "type": "MCQ",
  "marks": 2,
  "difficulty": "Medium",
  "context": "MoodMatch AI senses user emotion and recommends content accordingly..."
}

🤖 Models Used
gemma:2b (via Ollama) — lightweight LLM ideal for offline question generation.

You can replace it with heavier models like mistral or gemma:7b if RAM/VRAM allows.
