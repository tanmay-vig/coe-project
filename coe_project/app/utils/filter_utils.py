# app/utils/filter_utils.py

def smart_filter(docs, marks, difficulty, cognitive):
    """
    Filter documents based on marks, difficulty, and cognitive level.
    Falls back progressively if exact matches aren't found.
    """
    exact = [
        d for d in docs
        if d.metadata.get("marks") == marks
        and d.metadata.get("difficulty_level", "").lower() == difficulty.lower()
        and d.metadata.get("cognitive_level", "").lower() == cognitive.lower()
    ]
    if exact:
        return exact

    fallback = [
        d for d in docs
        if d.metadata.get("difficulty_level", "").lower() == difficulty.lower()
    ]
    if fallback:
        return fallback

    return docs[:3]
