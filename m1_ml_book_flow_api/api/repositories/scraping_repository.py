"""
Módulo de repositório para persistência de livros no banco de dados.

Este módulo contém funções para salvar dados de livros coletados via scraping
no banco de dados PostgreSQL usando SQLAlchemy.
"""
from sqlalchemy.orm import Session
from typing import List, Dict
from m1_ml_book_flow_api.core.models import BookDB
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def save_scraped_books(db: Session, books_data: List[Dict]) -> int:
    """
    Salva livros coletados via scraping no banco de dados.
    
    Para cada livro:
    - Se já existir (por título), atualiza os dados
    - Se não existir, cria um novo registro
    
    O commit é realizado imediatamente após processar todos os livros da lista,
    garantindo que os dados sejam persistidos no banco.
    
    Args:
        db (Session): Sessão do banco de dados SQLAlchemy
        books_data (List[Dict]): Lista de dicionários com dados dos livros a serem salvos.
                                Cada dicionário deve conter: title, author, year, category,
                                price, rating, available, image.
        
    Returns:
        int: Número total de livros salvos (criados + atualizados)
        
    Raises:
        SQLAlchemyError: Em caso de erro do banco de dados
        Exception: Em caso de erro inesperado (faz rollback automaticamente)
    """
    saved_count = 0
    updated_count = 0
    created_count = 0
    
    try:
        for i, book_data in enumerate(books_data, 1):
            try:
                # Verifica se o livro já existe no banco considerando título + imagem
                # Alguns títulos podem se repetir no site externo, mas cada produto
                # possui imagem/URL distinta. Usamos a combinação para evitar colisões.
                existing_book = (
                    db.query(BookDB)
                    .filter(
                        BookDB.title == book_data['title'],
                        BookDB.image == book_data.get('image')
                    )
                    .first()
                )
                
                if existing_book:
                    # Atualiza livro existente com novos dados
                    existing_book.author = book_data.get('author')
                    existing_book.year = book_data.get('year')
                    existing_book.category = book_data.get('category')
                    existing_book.price = book_data['price']
                    existing_book.rating = book_data.get('rating')
                    existing_book.available = book_data.get('available', True)
                    existing_book.image = book_data.get('image')
                    saved_count += 1
                    updated_count += 1
                else:
                    # Cria novo registro de livro no banco
                    new_book = BookDB(
                        title=book_data['title'],
                        author=book_data.get('author'),
                        year=book_data.get('year'),
                        category=book_data.get('category'),
                        price=book_data['price'],
                        rating=book_data.get('rating'),
                        available=book_data.get('available', True),
                        image=book_data.get('image')
                    )
                    db.add(new_book)
                    saved_count += 1
                    created_count += 1
                    
            except Exception as e:
                print(f"  ❌ Erro ao salvar livro '{book_data.get('title', 'unknown')}': {e}")
                logger.error(f"Erro ao salvar livro {book_data.get('title', 'unknown')}: {e}", exc_info=True)
                continue
        
        # Realiza commit imediato para este lote de livros
        db.flush()
        db.commit()
        
        if saved_count > 0:
            print(f"  ✅ Commit realizado: {created_count} novos, {updated_count} atualizados (total: {saved_count})")
            logger.info(f"Commit realizado com sucesso: {saved_count} livros salvos (criados: {created_count}, atualizados: {updated_count})")
        
        return saved_count
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erro do banco de dados ao salvar livros: {e}", exc_info=True)
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro inesperado ao salvar livros: {e}", exc_info=True)
        raise

