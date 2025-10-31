"""
Pacote core com componentes fundamentais da aplicação.

Este pacote contém módulos centrais da aplicação que fornecem funcionalidades
fundamentais como configuração de banco de dados, logging, tratamento de erros,
middlewares, segurança e modelos de dados.

Módulos disponíveis:
    - database: Configuração e gerenciamento de conexão com banco de dados PostgreSQL
    - models: Modelos SQLAlchemy para entidades do banco de dados
    - logger: Configuração de logging estruturado em JSON
    - middleware: Middlewares HTTP para logging, métricas e contexto
    - handlers: Handlers centralizados para tratamento de exceções
    - errors: Modelos de resposta padronizados para erros
    - exceptions: Exceções customizadas para diferentes tipos de erro HTTP
    - security: Funcionalidades de autenticação e autorização JWT
"""

