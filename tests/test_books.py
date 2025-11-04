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
    to_encode = {"sub": user_id, "type": "access"}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def auth_header():
    token = create_test_token("admin")
    return {"Authorization": f"Bearer {token}"}

def test_list_books(auth_header, mock_list_books_success):
    response = client.get("/api/v1/books", headers=auth_header)
    assert isinstance(response.json(), list)

def test_list_books_return_success(auth_header, mock_list_books_success):
    response = client.get("/api/v1/books", headers=auth_header)
    assert response.status_code == 200

def test_list_books_return_err(auth_header):
    response = client.get("/api/v1/books", headers=auth_header)
    assert response.status_code != 404

def test_list_books_is_empty(auth_header, mock_list_books_success):
    response = client.get("/api/v1/books", headers=auth_header)
    assert not len(response.json()) == 0

def test_get_book(auth_header, mock_get_book_success):
    response = client.get("/api/v1/books/1", headers=auth_header)
    assert isinstance(response.json(), dict)

def test_get_non_existent_book(auth_header, mock_get_book_not_found):
    response = client.get("/api/v1/books/5", headers=auth_header)
    assert response.status_code == 404

def test_search_books_for_title(auth_header, mock_search_books_success):
    response =  client.get("/api/v1/books/search?title=Livro A", headers=auth_header)
    assert isinstance(response.json(), list)

def test_search_books_for_category(auth_header, mock_search_books_success):
    response =  client.get("/api/v1/books/search?category=Romance", headers=auth_header)
    assert isinstance(response.json(), list)

def test_search_books_for_non_existent_title(auth_header, mock_search_books_empty):
    response = client.get("/api/v1/books/search?title=Livro D", headers=auth_header)
    assert response.status_code == 404

def test_search_books_for_non_existent_category(auth_header, mock_search_books_empty):
    response = client.get("/api/v1/books/search?category=Terror", headers=auth_header)
    assert response.status_code == 404

def test_search_books_for_non_existent_title_but_existent_category(auth_header, mock_search_books_empty):
    response = client.get("/api/v1/books/search?title=Livro D&category=Romance", headers=auth_header)
    assert response.status_code == 404

def test_search_books_for_non_existent_category_but_existent_title(auth_header, mock_search_books_empty):
    response = client.get("/api/v1/books/search?title=Livro A&category=Terror", headers=auth_header)
    assert response.status_code == 404

def test_search_books_for_non_existent_title_and_non_existent_category(auth_header, mock_search_books_empty):
    response = client.get("/api/v1/books/search?title=Livro D&category=Terror", headers=auth_header)
    assert response.status_code == 404

def test_get_categories(auth_header, mock_categories_success):
    response = client.get("/api/v1/categories", headers=auth_header)
    assert isinstance(response.json(), list)

def test_get_categories_is_empty(auth_header, mock_categories_empty):
    response = client.get("/api/v1/categories", headers=auth_header)
    assert response.status_code == 404

def test_health_ok(mock_health_ok):
    response = client.get("/api/v1/health")
    assert response.status_code == 200

def test_health_not_found(mock_health_not_found):
    response = client.get("/api/v1/health")
    assert response.status_code == 404

def test_stats_overview_ok(auth_header, mock_stats_overview_success):
    response = client.get("/api/v1/stats/overview", headers=auth_header)
    assert response.status_code == 200

def test_stats_overview_not_found(auth_header, mock_stats_overview_empty):
    response = client.get("/api/v1/stats/overview", headers=auth_header)
    assert response.status_code == 404

def test_stats_categories_ok(auth_header, mock_stats_categories_success):
    response = client.get("/api/v1/stats/categories", headers=auth_header)
    assert response.status_code == 200

def test_stats_categories_not_found(auth_header, mock_stats_categories_empty):
    response = client.get("/api/v1/stats/categories", headers=auth_header)
    assert response.status_code == 404

def test_top_rating_5(auth_header, mock_top_rating_success):
    response = client.get("/api/v1/books/top-rated?number_items=5", headers=auth_header)
    assert response.status_code == 200

def test_top_rating_15(auth_header, mock_top_rating_success):
    response = client.get("/api/v1/books/top-rated?number_items=15", headers=auth_header)
    assert response.status_code == 200

def test_top_rating_not_found(auth_header, mock_top_rating_empty):
    response = client.get("/api/v1/books/top-rated?number_items=5", headers=auth_header)
    assert response.status_code == 404

def test_with_zero_min_price(auth_header, mock_price_range_success):
    response = client.get("/api/v1/books/price_range?min=30.0", headers=auth_header)
    assert response.status_code == 200

def test_with_zero_max_price(auth_header, mock_price_range_success):
    response = client.get("/api/v1/books/price_range?max=30.0", headers=auth_header)
    assert response.status_code == 200

def test_with_range_price(auth_header, mock_price_range_success):
    response = client.get("/api/v1/books/price_range?min=30.0&max=40.0", headers=auth_header)
    assert response.status_code == 200