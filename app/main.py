from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List

from app.services.document_service import DocumentService

app = FastAPI(title="RAG Pipeline")

document_service = DocumentService()

@app.get("/")
async def root():
    return {"message": "RAG Pipeline API is running"}

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    if len(files) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 documents allowed")
    try:
        result = await document_service.process_documents(files)
        return {"status": "success", "processed": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_documents(question: str):
    try:
        answer = document_service.search_documents(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

