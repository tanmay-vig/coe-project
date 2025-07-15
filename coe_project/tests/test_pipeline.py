from app.services.ocr_utils import refine_text
from app.services.question_gen import split_text_into_chunks

def test_refine_text():
    noisy = "This is a \n messy!!@@ string123\n"
    clean = refine_text(noisy)
    assert isinstance(clean, str)
    assert "\n" not in clean
    assert "@" not in clean
    assert "123" not in clean
    assert "messy" in clean.lower()

def test_chunking():
    text = "This is a test document. " * 50  # Should be enough for multiple chunks
    chunks = split_text_into_chunks(text)
    assert isinstance(chunks, list)
    assert len(chunks) > 1
    assert all(hasattr(chunk, "page_content") for chunk in chunks)
