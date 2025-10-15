import pytest
from fastapi.testclient import TestClient
from app.main import app
from fastapi import UploadFile
from io import BytesIO

client = TestClient(app)

def test_upload_single_file():
    files = {"files": ("example.txt", b"Hello World", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
    assert json_data["status"] == "success"
    assert len(json_data["processed"]) == 1
    assert json_data["processed"][0]["filename"] == "example.txt"

def test_upload_multiple_files():
    files = [
        ("files", ("file1.txt", b"Content 1", "text/plain")),
        ("files", ("file2.txt", b"Content 2", "text/plain")),
    ]
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data["processed"]) == 2

def test_upload_too_many_files():
    # Create 21 files to exceed the limit of 20
    files = [("files", (f"file{i}.txt", b"data", "text/plain")) for i in range(21)]
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "Maximum 20 documents allowed" in response.text
