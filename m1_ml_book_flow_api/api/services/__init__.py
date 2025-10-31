"""
Pacote de serviços para lógica de negócio da API.

Este pacote contém módulos de serviço que implementam a lógica de negócio da aplicação,
seguindo o padrão Service Layer. Cada serviço é responsável por orquestrar operações
relacionadas a uma entidade ou funcionalidade específica, funcionando como camada
intermediária entre as rotas (controllers) e os repositórios (data access).

Módulos disponíveis:
    - books_service: Lógica de negócio para gerenciamento de livros (listagem, busca, filtros, detalhes)
    - auth_service: Lógica de negócio para autenticação de usuários (login, refresh token)
    - categories_service: Lógica de negócio para listagem de categorias de livros
    - health_service: Lógica de negócio para health check da API
    - stats_overview_service: Lógica de negócio para estatísticas gerais dos livros
    - stats_categories_service: Lógica de negócio para estatísticas agrupadas por categoria
    - top_rating_service: Lógica de negócio para livros mais bem avaliados (top rated)
    - scraping_service: Lógica de negócio para web scraping de livros (extração de dados)
    - scraping_trigger_service: Lógica de negócio para orquestração do processo de scraping
"""

