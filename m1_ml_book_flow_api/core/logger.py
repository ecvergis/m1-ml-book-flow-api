import logging

# Configuração básica do logging
logging.basicConfig(
    level=logging.DEBUG,  # nível mínimo de log (DEBUG mostra tudo)
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
)

# Criar logger padrão
Logger = logging.getLogger("BookFlow")  # você pode dar um nome da sua aplicação
