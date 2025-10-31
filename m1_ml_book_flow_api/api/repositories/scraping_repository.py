from sqlalchemy.orm import Session
from typing import List, Dict
from m1_ml_book_flow_api.core.models import BookDB
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def save_scraped_books(db: Session, books_data: List[Dict]) -> int:
    """
    Save scraped books to database.
    Saves immediately and commits at the end.
    Returns the number of books saved.
    """
    saved_count = 0
    updated_count = 0
    created_count = 0
    
    try:
        for i, book_data in enumerate(books_data, 1):
            try:
                # Check if book already exists by title
                existing_book = db.query(BookDB).filter(BookDB.title == book_data['title']).first()
                
                if existing_book:
                    # Update existing book
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
                    # Create new book
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
                logger.error(f"Error saving book {book_data.get('title', 'unknown')}: {e}", exc_info=True)
                continue
        
        # Commit immediately for this batch
        db.flush()
        db.commit()
        
        if saved_count > 0:
            print(f"  ✅ Commit realizado: {created_count} novos, {updated_count} atualizados (total: {saved_count})")
            logger.info(f"Successfully committed {saved_count} books to database (created: {created_count}, updated: {updated_count})")
        
        return saved_count
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while saving books: {e}", exc_info=True)
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while saving books: {e}", exc_info=True)
        raise

