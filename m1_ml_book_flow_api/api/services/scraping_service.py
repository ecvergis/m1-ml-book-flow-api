import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin, urlparse
import re

BASE_URL = "https://books.toscrape.com"
CATALOGUE_URL = f"{BASE_URL}/catalogue"

def get_total_pages() -> int:
    """Get total number of pages to scrape"""
    try:
        response = requests.get(f"{BASE_URL}/index.html", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        pagination = soup.find('ul', class_='pager')
        if pagination:
            page_numbers = pagination.find_all('li', class_='current')
            if page_numbers:
                total_text = page_numbers[0].text.strip()
                import re
                match = re.search(r'of (\d+)', total_text)
                if match:
                    return int(match.group(1))
    except:
        pass
    return 0

def scrape_page(page: int, total_pages: int = 0) -> List[Dict]:
    """
    Scrape a single page and return books data.
    Returns empty list if page doesn't exist.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    if page == 1:
        url = f"{BASE_URL}/index.html"
    else:
        url = f"{CATALOGUE_URL}/page-{page}.html"
    
    try:
        print(f"\n📄 Processando página {page}/{total_pages if total_pages > 0 else '?'}...")
        logger.info(f"Scraping page {page}/{total_pages if total_pages > 0 else '?'}...")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        
        if not books:
            print(f"⚠️  Nenhum livro encontrado na página {page}")
            logger.info(f"No books found on page {page}")
            return []
        
        print(f"✅ Encontrados {len(books)} livros na página {page}")
        logger.info(f"Found {len(books)} books on page {page}")
        
        books_data = []
        for i, book in enumerate(books, 1):
            book_data = extract_book_data(book, BASE_URL)
            if book_data:
                books_data.append(book_data)
            if i % 10 == 0:
                print(f"  ⏳ Processados {i}/{len(books)} livros da página")
                logger.info(f"Processed {i}/{len(books)} books from page {page}")
        
        print(f"✅ Página {page} processada! {len(books_data)} livros extraídos")
        logger.info(f"Page {page} completed. Extracted {len(books_data)} books")
        
        return books_data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao buscar página {page}: {e}")
        logger.error(f"Error fetching page {page}: {e}")
        return []

def has_next_page(page: int) -> bool:
    """Check if there's a next page to scrape"""
    try:
        if page == 1:
            url = f"{BASE_URL}/index.html"
        else:
            url = f"{CATALOGUE_URL}/page-{page}.html"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        next_button = soup.find('li', class_='next')
        return next_button is not None
    except:
        return False

def extract_book_data(book_element, base_url: str) -> Dict:
    """Extract book data from a single book element"""
    try:
        # Title
        title_elem = book_element.find('h3')
        title = title_elem.find('a')['title'] if title_elem and title_elem.find('a') else None
        
        # Price
        price_elem = book_element.find('p', class_='price_color')
        price_str = price_elem.text.strip() if price_elem else "£0.00"
        price = parse_price(price_str)
        
        # Rating
        rating_elem = book_element.find('p', class_='star-rating')
        rating = parse_rating(rating_elem) if rating_elem else None
        
        # Availability
        availability_elem = book_element.find('p', class_='instock')
        available = True
        if availability_elem:
            availability_text = availability_elem.text.strip().lower()
            available = 'in stock' in availability_text
        
        # Image
        image_elem = book_element.find('img')
        image_url = None
        if image_elem and image_elem.get('src'):
            image_relative = image_elem['src']
            image_url = urljoin(base_url, image_relative)
        
        # Category - need to visit book detail page
        link_elem = book_element.find('h3')
        book_detail_url = None
        if link_elem and link_elem.find('a'):
            book_detail_relative = link_elem.find('a')['href']
            # The href may be relative to catalogue or absolute
            if book_detail_relative.startswith('..'):
                book_detail_url = urljoin(BASE_URL + '/', book_detail_relative.replace('../', ''))
            elif book_detail_relative.startswith('catalogue/'):
                book_detail_url = urljoin(BASE_URL + '/', book_detail_relative)
            else:
                book_detail_url = urljoin(CATALOGUE_URL + '/', book_detail_relative)
        
        category = None
        author = None
        year = None
        
        # Fetch book detail page for category, author, and year
        if book_detail_url:
            try:
                detail_response = requests.get(book_detail_url, timeout=5)
                detail_response.raise_for_status()
                detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                
                # Category
                breadcrumb = detail_soup.find('ul', class_='breadcrumb')
                if breadcrumb:
                    category_links = breadcrumb.find_all('a')
                    if len(category_links) >= 2:
                        category = category_links[1].text.strip()
                
                # Author
                product_info = detail_soup.find('article', class_='product_page')
                if product_info:
                    table = product_info.find('table', class_='table')
                    if table:
                        rows = table.find_all('tr')
                        for row in rows:
                            th = row.find('th')
                            td = row.find('td')
                            if th and td:
                                if 'author' in th.text.lower():
                                    author = td.text.strip()
                                elif 'number of pages' in th.text.lower():
                                    # Try to extract year from description or other fields
                                    pass
                
            except Exception as e:
                print(f"Error fetching book details from {book_detail_url}: {e}")
        
        if not title or price is None:
            return None
        
        return {
            'title': title,
            'author': author,
            'year': year,
            'category': category,
            'price': price,
            'rating': rating,
            'available': available,
            'image': image_url
        }
        
    except Exception as e:
        print(f"Error extracting book data: {e}")
        return None

def parse_price(price_str: str) -> float:
    """Parse price string (e.g., '£51.77') to float"""
    try:
        # Remove currency symbols and extract number
        price_clean = re.sub(r'[^\d.]', '', price_str)
        return float(price_clean)
    except:
        return 0.0

def parse_rating(rating_elem) -> float:
    """Parse star rating to float (e.g., 'Three' -> 3.0)"""
    rating_map = {
        'One': 1.0,
        'Two': 2.0,
        'Three': 3.0,
        'Four': 4.0,
        'Five': 5.0
    }
    
    rating_classes = rating_elem.get('class', [])
    for cls in rating_classes:
        if cls in rating_map:
            return rating_map[cls]
    
    return None

