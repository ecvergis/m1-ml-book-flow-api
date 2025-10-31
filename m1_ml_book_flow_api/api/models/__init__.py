"""
Módulo de modelos Pydantic para a API.

Este pacote contém todos os modelos Pydantic usados para:
- Validação de dados de entrada (request bodies)
- Serialização de dados de saída (response models)
- Estruturação de dados entre camadas da aplicação

Modelos disponíveis:
- Book: Modelo básico de livro
- BookDetails: Modelo com detalhes completos de um livro
- Auth: Modelo de credenciais de autenticação
- RefreshToken: Modelo para renovação de token
- HealthResponse: Modelo de resposta do health check
- StatsOverview: Modelo de estatísticas gerais
- StatsCategories: Modelo de estatísticas por categoria
- TopRatedBook: Modelo de livro top avaliado
"""

