
from app.core.config import settings

def chunk_text(text, chunk_size=None):
    """Split text into chunks of chunk_size"""
    if chunk_size is None:
        chunk_size = settings.CHUNK_SIZE
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
