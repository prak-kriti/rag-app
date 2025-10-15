import os
from typing import List
from fastapi import UploadFile

from app.services.embeddings import EmbeddingGenerator
from app.services.vectorstore import VectorStore
from app.services.llm_client import LLMClient

class DocumentService:
    def __init__(self):
        self.embedder = EmbeddingGenerator()
        self.vectorstore = VectorStore()
        self.llm = LLMClient()
        self.documents = []  # Metadata storage

    async def process_documents(self, files: List[UploadFile]):
        results = []
        for file in files:
            content = await file.read()
            text = content.decode("utf-8", errors="ignore")  # Decode file
            # Chunking (simple split, can improve)
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
            embeddings = self.embedder.generate_batch(chunks)
            self.vectorstore.add_embeddings(embeddings, chunks)
            self.documents.append({
                "filename": file.filename,
                "num_chunks": len(chunks)
            })
            results.append({"filename": file.filename, "chunks": len(chunks)})
            file.file.seek(0)  # reset pointer
        return results

    def search_documents(self, query: str):
        query_emb = self.embedder.generate(query)
        relevant_chunks = self.vectorstore.query(query_emb)
        answer = self.llm.generate(query, relevant_chunks)
        return answer
