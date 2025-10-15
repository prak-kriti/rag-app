import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_basic():
    response = client.post("/query", json={"question": "What is AI?"})
    assert response.status_code == 200
    json_data = response.json()
    assert "question" in json_data
    assert json_data["question"] == "What is AI?"
    assert "answer" in json_data

def test_query_empty():
    response = client.post("/query", json={"question": ""})
    assert response.status_code == 200  # or whatever your service returns for empty question
    json_data = response.json()
    assert "answer" in json_data
