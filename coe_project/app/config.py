# app/config.py

from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FAISS_INDEX_PATH = DATA_DIR / "faiss_index"
QUESTIONS_JSON_PATH = DATA_DIR / "questions.json"
UPLOADS_DIR = DATA_DIR / "uploads"
SAMPLE_PDFS_DIR = DATA_DIR / "sample_pdfs"

# Model Configurations
OLLAMA_MODEL_NAME = "gemma:2b"
TEMPERATURE = 0.1
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RESULTS = 4

# Metadata Keys (used in embedding store and search)
METADATA_KEYS = [
    "topic",
    "subtopic",
    "marks",
    "question_type",
    "difficulty_level",
    "cognitive_level",
    "chunk_id",
    "time"
]

# Optional Flags
ENABLE_LOGGING = True
USE_ADVANCED_CLASSIFIER = True  # toggle if using LangChain toolchains
