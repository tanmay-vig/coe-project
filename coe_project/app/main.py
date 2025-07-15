# app/main.py

from fastapi import FastAPI
from app.routes import router as api_router
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = FastAPI(title="RAG PDF Chatbot")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace with ["http://localhost:3000"] if you use a specific frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")
# FastAPI entry point
