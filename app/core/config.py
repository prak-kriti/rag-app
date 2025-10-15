import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv(dotenv_path="/content/rag-app/.env")

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "vector_store")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))

settings = Settings()
