import pytest
from unittest.mock import patch


def sample_book(
    id: int = 1,
    title: str = "Livro A",
    author: str = "Autor A",
    year: int = 2020,
    category: str = "Ficção",
    price: float = 29.9,
    rating: float = 4.5,
    available: bool = True,
    image: str = "http://example.com/img.jpg",
):
    return {
        'id': id,
        'title': title,
        'author': author,
        'year': year,
        'category': category,
        'price': price,
        'rating': rating,
        'available': available,
        'image': image,
    }

def sample_book_details():
    return {
        'id': 1,
        'title': 'Livro A',
        'author': 'Autor A',
        'year': 2021,
        'score': 4.2,
        'price_without_tax': 35.9,
        'price_with_tax': 39.9,
        'tax': 4.0,
        'product_type': 'Livro',
        'upc': 'abc123',
        'available': True,
        'number_reviews': 12
    }

def sample_categories():
    return ['Ficção', 'Romance', 'Terror']


def sample_stats_overview():
    return {
        'total_books': 3,
        'middle_price': 35.5,
        'distribution_ratings': {
            '4.0': 1,
            '4.5': 1,
            '5.0': 1
        }
    }

def sample_stats_categories():
    return [
        {'category_name': 'Ficção', 'quantity_books': 5, 'category_price': 39.9},
        {'category_name': 'Tecnologia', 'quantity_books': 3, 'category_price': 59.9}
    ]

def sample_top_rated_list(n: int = 3):
    base = [
        {'title': 'Livro X', 'rating': 4.8},
        {'title': 'Livro Y', 'rating': 4.7},
        {'title': 'Livro Z', 'rating': 4.6},
    ]
    return base[:n]

@pytest.fixture
def mock_list_books_success():
    with patch('m1_ml_book_flow_api.api.services.books_service.list_books', return_value=[sample_book()]):
        yield

@pytest.fixture
def mock_get_book_success():
    with patch('m1_ml_book_flow_api.api.services.books_service.get_book_by_id', return_value=sample_book_details()):
        yield

@pytest.fixture
def mock_search_books_success():
    with patch('m1_ml_book_flow_api.api.services.books_service.search_books_by', return_value=[sample_book(title="Livro A", category="Romance")]):
        yield

@pytest.fixture
def mock_categories_success():
    with patch('m1_ml_book_flow_api.api.services.categories_service.list_categories', return_value=sample_categories()):
        yield

@pytest.fixture
def mock_stats_overview_success():
    with patch('m1_ml_book_flow_api.api.services.stats_overview_service.get_stats_overview', return_value=sample_stats_overview()):
        yield

@pytest.fixture
def mock_stats_categories_success():
    with patch('m1_ml_book_flow_api.api.services.stats_categories_service.get_stats_categories', return_value=sample_stats_categories()):
        yield

@pytest.fixture
def mock_top_rating_success():
    with patch('m1_ml_book_flow_api.api.services.top_rating_service.get_top_rating', return_value=sample_top_rated_list()):
        yield

@pytest.fixture
def mock_price_range_success():
    with patch('m1_ml_book_flow_api.api.services.books_service.search_books_by_range_price', return_value=[sample_book(price=35.0)]):
        yield

@pytest.fixture
def mock_search_books_empty():
    with patch('m1_ml_book_flow_api.api.services.books_service.search_books_by', return_value=[]):
        yield

@pytest.fixture
def mock_categories_empty():
    with patch('m1_ml_book_flow_api.api.services.categories_service.list_categories', return_value=[]):
        yield

@pytest.fixture
def mock_stats_overview_empty():
    with patch('m1_ml_book_flow_api.api.services.stats_overview_service.get_stats_overview', return_value=None):
        yield

@pytest.fixture
def mock_stats_categories_empty():
    with patch('m1_ml_book_flow_api.api.services.stats_categories_service.get_stats_categories', return_value={}):
        yield

@pytest.fixture
def mock_top_rating_empty():
    with patch('m1_ml_book_flow_api.api.services.top_rating_service.get_top_rating', return_value=[]):
        yield

@pytest.fixture
def mock_health_ok():
    with patch('m1_ml_book_flow_api.api.services.health_service.get_books_count', return_value=10):
        yield

@pytest.fixture
def mock_health_not_found():
    with patch('m1_ml_book_flow_api.api.services.health_service.get_books_count', return_value=0):
        yield

@pytest.fixture
def mock_get_book_not_found():
    with patch('m1_ml_book_flow_api.api.services.books_service.get_book_by_id', return_value=None):
        yield