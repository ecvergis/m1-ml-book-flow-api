from typing import Dict
from sqlalchemy.orm import Session
from m1_ml_book_flow_api.core.logger import get_logger, log_error
from m1_ml_book_flow_api.api.services.scraping_service import scrape_page, get_total_pages, has_next_page
from m1_ml_book_flow_api.api.repositories.scraping_repository import save_scraped_books
from fastapi import HTTPException, status

scraping_logger = get_logger("scraping_service")

def trigger_scraping(db: Session) -> Dict:
    """
    Trigger web scraping process and save books to database.
    Saves page by page to avoid memory issues and data loss.
    Returns a dictionary with scraping results.
    """
    print("\n" + "=" * 60)
    print("🚀 INICIANDO PROCESSO DE SCRAPING")
    print("=" * 60)
    scraping_logger.info("Starting web scraping", extra={"event": "scraping_start"})
    
    total_scraped = 0
    total_saved = 0
    page = 1
    
    try:
        # Get total pages
        print("📥 Conectando ao site books.toscrape.com...")
        total_pages = get_total_pages()
        print(f"📚 Total de páginas estimadas: {total_pages if total_pages > 0 else '?'}")
        print("-" * 60)
        scraping_logger.info("Scraping books from books.toscrape.com", extra={"event": "scraping_fetch", "total_pages": total_pages})
        
        # Process and save page by page
        while True:
            # Scrape current page
            books_data = scrape_page(page, total_pages)
            
            if not books_data:
                print(f"\n⚠️  Nenhum livro encontrado na página {page}, encerrando...")
                break
            
            total_scraped += len(books_data)
            
            # Save current page immediately
            print(f"\n💾 Salvando {len(books_data)} livros da página {page} no banco...")
            scraping_logger.info(
                f"Saving page {page} to database",
                extra={"event": "scraping_save_page", "page": page, "books_count": len(books_data)}
            )
            
            try:
                saved_count = save_scraped_books(db, books_data)
                total_saved += saved_count
                print(f"✅ Página {page} salva! {saved_count} livros salvos (Total acumulado: {total_saved})")
                scraping_logger.info(
                    f"Page {page} saved successfully",
                    extra={"event": "scraping_page_saved", "page": page, "saved_count": saved_count, "total_saved": total_saved}
                )
            except Exception as db_error:
                print(f"❌ ERRO ao salvar página {page}: {str(db_error)}")
                scraping_logger.error(
                    f"Error saving page {page} to database: {str(db_error)}",
                    extra={"event": "scraping_save_page_error", "page": page, "error": str(db_error)},
                    exc_info=True
                )
                # Continue with next page even if this one fails
                print(f"⚠️  Continuando com próxima página...")
            
            # Check if there's a next page
            if not has_next_page(page):
                print(f"\n🏁 Todas as páginas foram processadas!")
                break
            
            page += 1
        
        # Final summary
        print("\n" + "=" * 60)
        print(f"✅ SCRAPING CONCLUÍDO!")
        print(f"📊 Total de livros coletados: {total_scraped}")
        print(f"💾 Total de livros salvos: {total_saved}")
        print("=" * 60)
        
        scraping_logger.info(
            f"Scraping completed",
            extra={
                "event": "scraping_success",
                "scraped_count": total_scraped,
                "saved_count": total_saved,
                "pages_processed": page
            }
        )
        
        if total_saved == 0:
            scraping_logger.warning(
                "No books saved",
                extra={"event": "scraping_empty"}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Nenhum livro foi salvo no banco de dados"
            )
        
        return {
            "message": "Scraping concluído com sucesso",
            "scraped_count": total_scraped,
            "saved_count": total_saved,
            "pages_processed": page
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="trigger_scraping",
            event="scraping_error"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao executar scraping: {str(e)}"
        )

