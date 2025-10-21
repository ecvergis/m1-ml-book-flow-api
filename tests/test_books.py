import pytest
from fastapi.testclient import TestClient
from m1_ml_book_flow_api.main import app

client = TestClient(app)

def test_list_books():
    response = client.get("/api/v1/books")
    assert isinstance(response.json(), list)

def test_list_books_return_success():
    response = client.get("/api/v1/books")
    assert response.status_code == 200

def test_list_books_return_err():
    response = client.get("/api/v1/books")
    assert response.status_code != 404