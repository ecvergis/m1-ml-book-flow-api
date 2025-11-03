"""
Módulo de serviço para web scraping de livros.

Este módulo contém funções para realizar web scraping do site books.toscrape.com,
extraindo informações sobre livros como título, preço, categoria, autor, rating, etc.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin, urlparse
import re

# URLs base do site de scraping
BASE_URL = "https://books.toscrape.com"
CATALOGUE_URL = f"{BASE_URL}/catalogue"

def get_total_pages() -> int:
    """
    Obtém o número total de páginas disponíveis para scraping.
    
    Returns:
        int: Número total de páginas encontradas. Retorna 0 se não conseguir determinar.
    """
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
    Processa uma única página e extrai dados dos livros.
    
    Args:
        page (int): Número da página a ser processada (1 para primeira página)
        total_pages (int, optional): Total de páginas estimadas para exibição no log
        
    Returns:
        List[Dict]: Lista de dicionários contendo dados dos livros extraídos.
                   Retorna lista vazia se a página não existir ou não contiver livros.
                   
    Cada dicionário contém:
        - title: Título do livro
        - author: Nome do autor
        - year: Ano de publicação
        - category: Categoria do livro
        - price: Preço em float
        - rating: Avaliação em estrelas (float de 1.0 a 5.0)
        - available: Se está disponível (boolean)
        - image: URL da imagem da capa
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
    """
    Verifica se existe uma próxima página para processar.
    
    Args:
        page (int): Número da página atual
        
    Returns:
        bool: True se existe próxima página, False caso contrário
    """
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
    """
    Extrai dados de um único livro a partir do elemento HTML.
    
    Esta função busca na página de listagem e na página de detalhes do livro
    para extrair todas as informações disponíveis.
    
    Args:
        book_element: Elemento BeautifulSoup representando um artigo de livro
        base_url (str): URL base do site para construção de URLs absolutas
        
    Returns:
        Dict: Dicionário com dados do livro ou None se não conseguir extrair dados essenciais.
    """
    try:
        # Extrai título do livro
        title_elem = book_element.find('h3')
        title = title_elem.find('a')['title'] if title_elem and title_elem.find('a') else None
        
        # Extrai preço do livro
        price_elem = book_element.find('p', class_='price_color')
        price_str = price_elem.text.strip() if price_elem else "£0.00"
        price = parse_price(price_str)
        
        # Extrai avaliação (rating em estrelas)
        rating_elem = book_element.find('p', class_='star-rating')
        rating = parse_rating(rating_elem) if rating_elem else None
        
        # Extrai disponibilidade do estoque
        availability_elem = book_element.find('p', class_='instock')
        available = True
        if availability_elem:
            availability_text = availability_elem.text.strip().lower()
            available = 'in stock' in availability_text
        
        # Extrai URL da imagem da capa
        image_elem = book_element.find('img')
        image_url = None
        if image_elem and image_elem.get('src'):
            image_relative = image_elem['src']
            image_url = urljoin(base_url, image_relative)
        
        # Para obter categoria, autor e outros detalhes, precisa visitar a página de detalhes do livro
        link_elem = book_element.find('h3')
        book_detail_url = None
        if link_elem and link_elem.find('a'):
            book_detail_relative = link_elem.find('a')['href']
            # O href pode ser relativo ao catálogo ou absoluto
            if book_detail_relative.startswith('..'):
                book_detail_url = urljoin(BASE_URL + '/', book_detail_relative.replace('../', ''))
            elif book_detail_relative.startswith('catalogue/'):
                book_detail_url = urljoin(BASE_URL + '/', book_detail_relative)
            else:
                book_detail_url = urljoin(CATALOGUE_URL + '/', book_detail_relative)
        
        category = None
        author = None
        year = None
        
        # Busca a página de detalhes do livro para obter categoria, autor e ano
        if book_detail_url:
            try:
                detail_response = requests.get(book_detail_url, timeout=5)
                detail_response.raise_for_status()
                detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                
                # Extrai categoria do breadcrumb (navegação)
                breadcrumb = detail_soup.find('ul', class_='breadcrumb')
                if breadcrumb:
                    category_links = breadcrumb.find_all('a')
                    # Se há 3 ou mais links, pega o terceiro (categoria específica como Romance)
                    # Se há apenas 2 links, pega o segundo (Books)
                    if len(category_links) >= 3:
                        category = category_links[2].text.strip()
                    elif len(category_links) >= 2:
                        category = category_links[1].text.strip()
                
                # Extrai autor da tabela de informações do produto
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
                                    # Tentativa de extrair ano da descrição ou outros campos
                                    pass
                
            except Exception as e:
                print(f"Erro ao buscar detalhes do livro em {book_detail_url}: {e}")
        
        # Validação: título e preço são obrigatórios
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
        print(f"Erro ao extrair dados do livro: {e}")
        return None

def parse_price(price_str: str) -> float:
    """
    Converte string de preço para float.
    
    Remove símbolos de moeda e extrai apenas o valor numérico.
    Exemplo: '£51.77' -> 51.77
    
    Args:
        price_str (str): String com o preço (ex: '£51.77')
        
    Returns:
        float: Preço como número float. Retorna 0.0 em caso de erro.
    """
    try:
        # Remove símbolos de moeda e extrai apenas o número
        price_clean = re.sub(r'[^\d.]', '', price_str)
        return float(price_clean)
    except:
        return 0.0

def parse_rating(rating_elem) -> float:
    """
    Converte elemento de avaliação em estrelas para número float.
    
    Converte classes CSS como 'Three' para o valor numérico correspondente.
    Exemplo: 'Three' -> 3.0
    
    Args:
        rating_elem: Elemento BeautifulSoup com classes de avaliação
        
    Returns:
        float: Avaliação de 1.0 a 5.0 ou None se não conseguir determinar
    """
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

