from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from m1_ml_book_flow_api.main import app
from m1_ml_book_flow_api.core.security.jwt import create_test_token
from m1_ml_book_flow_api.core.security.security import SECRET_KEY, ALGORITHM
import jwt
from datetime import datetime, timedelta

client = TestClient(app)

def create_test_token(user_id: str, expires_delta: timedelta = None):
    to_encode = {"sub": user_id}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def auth_header():
    token = create_test_token("admin")
    return {"Authorization": f"Bearer {token}"}

def test_list_books(auth_header):
    response = client.get("/api/v1/books", headers=auth_header)
    assert isinstance(response.json(), list)

def test_list_books_return_success(auth_header):
    response = client.get("/api/v1/books", headers=auth_header)
    assert response.status_code == 200

def test_list_books_return_err(auth_header):
    response = client.get("/api/v1/books", headers=auth_header)
    assert response.status_code != 404

def test_list_books_is_empty(auth_header):
    response = client.get("/api/v1/books", headers=auth_header)
    assert not len(response.json()) == 0

def test_get_book(auth_header):
    response = client.get("/api/v1/books/1", headers=auth_header)
    assert isinstance(response.json(), dict)

def test_get_non_existent_book(auth_header):
    response = client.get("/api/v1/books/2", headers=auth_header)
    assert response.status_code == 404

def test_search_books_for_title(auth_header):
    response =  client.get("/api/v1/books/search?title=Livro A", headers=auth_header)
    assert isinstance(response.json(), list)

def test_search_books_for_category(auth_header):
    response =  client.get("/api/v1/books/search?category=Romance", headers=auth_header)
    assert isinstance(response.json(), list)

def test_search_books_for_non_existent_title(auth_header):
    response = client.get("/api/v1/books/search?title=Livro D", headers=auth_header)
    assert not len(response.json()) == 0

def test_search_books_for_non_existent_category(auth_header):
    response = client.get("/api/v1/books/search?category=Terror", headers=auth_header)
    assert not len(response.json()) == 0

def test_search_books_for_non_existent_title_but_existent_category(auth_header):
    response = client.get("/api/v1/books/search?title=Livro D&category=Romance", headers=auth_header)
    assert isinstance(response.json(), list)

def test_search_books_for_non_existent_category_but_existent_title(auth_header):
    response = client.get("/api/v1/books/search?title=Livro A&category=Terror", headers=auth_header)
    assert isinstance(response.json(), list)

def test_search_books_for_non_existent_title_and_non_existent_category(auth_header):
    response = client.get("/api/v1/books/search?title=Livro D&category=Terror", headers=auth_header)
    assert not len(response.json()) == 0

def test_get_categories(auth_header):
    response = client.get("/api/v1/categories", headers=auth_header)
    assert isinstance(response.json(), list)

def test_get_categories_is_empty(auth_header):
    response = client.get("/api/v1/categories", headers=auth_header)
    assert response.status_code == 404

def test_health_ok():
    with patch("m1_ml_book_flow_api.api.repositories.health_repository.get_books_count", return_value=3):
        response = client.get("/api/v1/health")
        assert response.status_code == 200

def test_health_not_found():
    with patch("m1_ml_book_flow_api.api.repositories.health_repository.get_books_count", return_value=0):
        response = client.get("/api/v1/health")
        assert response.status_code == 404