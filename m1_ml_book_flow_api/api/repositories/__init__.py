"""
Pacote de repositórios para acesso a dados.

Este pacote contém módulos de repositório que implementam a camada de acesso a dados
da aplicação, seguindo o padrão Repository. Cada repositório é responsável por
operações de leitura/escrita relacionadas a uma entidade específica.

Módulos disponíveis:
    - books_repository: Operações relacionadas a livros (busca, listagem, filtros)
    - auth_repository: Validação de credenciais de usuários
    - categories_repository: Listagem de categorias de livros
    - health_repository: Informações para health check
    - stats_overview_repository: Estatísticas gerais do sistema
    - stats_categories_repository: Estatísticas agrupadas por categoria
    - top_rating_repository: Livros mais bem avaliados (top rated)
    - scraping_repository: Persistência de livros coletados via web scraping
"""

