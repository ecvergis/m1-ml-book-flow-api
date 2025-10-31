"""
Módulo de repositório para autenticação de usuários.

Este módulo contém funções para validação de credenciais de usuários durante o login.
Usa uma base de dados mock simples em memória.

Nota: Esta implementação usa dados mock. Em produção, estas funções devem ser
adaptadas para acessar um banco de dados de usuários com senhas criptografadas.
"""
from m1_ml_book_flow_api.api.models.Auth import Auth

# Base de dados mock de usuários (username -> password)
# Em produção, as senhas devem estar criptografadas (hash)
USERS_DB = {"admin": "password123"}
# USERS_DB = {
#     "username": "admin",
#     "password": "password123"
# }

def login_user(user: Auth):
    """
    Valida credenciais de um usuário para login.

    Verifica se o username existe na base de dados e se a senha corresponde.
    A comparação de senha é feita de forma direta (texto plano).

    Args:
        user (Auth): Objeto Auth contendo username e password a serem validados.

    Returns:
        Auth: Retorna o objeto user se as credenciais forem válidas, None caso contrário.
    """
    if user.username not in USERS_DB or USERS_DB[user.username] != user.password:
        return None
    else:
        return user
