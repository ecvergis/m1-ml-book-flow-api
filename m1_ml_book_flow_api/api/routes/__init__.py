"""
Pacote de rotas para endpoints da API.

Este pacote contém módulos de rotas que definem os endpoints da API REST,
seguindo o padrão de rotas do FastAPI. Cada módulo é responsável por rotas
relacionadas a uma entidade ou funcionalidade específica.

Módulos disponíveis:
    - books: Rotas para gerenciamento de livros (listagem, busca, filtros, detalhes)
    - auth: Rotas para autenticação de usuários (login, refresh token)
    - categories: Rotas para listagem de categorias de livros
    - health: Rotas para health check da API
    - stats_overview: Rotas para estatísticas gerais dos livros
    - stats_categories: Rotas para estatísticas agrupadas por categoria
    - top_rating: Rotas para livros mais bem avaliados (top rated)
    - scraping: Rotas para web scraping de livros
"""

