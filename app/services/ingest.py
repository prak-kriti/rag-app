import os
import faiss
import numpy as np
from PyPDF2 import PdfReader
from app.services.chunker import chunk_text
from app.core.config import settings

# Mock embeddings function to avoid API calls for now
def mock_embeddings(text_chunks, dimension=768):
    return [np.random.rand(dimension).astype("float32") for _ in text_chunks]

class DocumentIngestor:
    def __init__(self):
        self.index_path = settings.FAISS_INDEX_PATH
        os.makedirs(self.index_path, exist_ok=True)
        self.index_file = os.path.join(self.index_path, "doc_index.faiss")
        self.meta_file = os.path.join(self.index_path, "chunks.txt")
        self.dimension = 768

        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)

    def load_pdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    def process_document(self, pdf_path):
        text = self.load_pdf(pdf_path)
        chunks = chunk_text(text)
        embeddings = mock_embeddings(chunks)
        self.save_to_faiss(chunks, embeddings)
        print(f"✅ Processed {len(chunks)} chunks from {pdf_path}")

    def save_to_faiss(self, chunks, embeddings):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        faiss.write_index(self.index, self.index_file)

        with open(self.meta_file, "a", encoding="utf-8") as f:
            for c in chunks:
                f.write(c.replace("\n", " ") + "\n")
