# m1-ml-book-flow-api

## Docker

### Build
```bash
docker build -t m1-ml-book-flow-api:latest .
```

### Run
```bash
docker run --rm -p 8000:8000 \
  -e JWT_SECRET_KEY="supersecretkey" \
  -e UVICORN_HOST="0.0.0.0" \
  -e UVICORN_PORT="8000" \
  -e UVICORN_WORKERS="2" \
  --name m1-ml-book-flow-api m1-ml-book-flow-api:latest
```

- Swagger: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`
- Metrics: `http://127.0.0.1:8000/metrics`

### Environment variables
- `JWT_SECRET_KEY` (default: `supersecretkey`)
- `UVICORN_HOST` (default: `0.0.0.0`)
- `UVICORN_PORT` (default: `8000`)
- `UVICORN_WORKERS` (default: `2`)

### Compose (docker-compose)
1) Crie um arquivo `.env` na raiz com as variáveis (IMPORTANTE: todas as variáveis são obrigatórias):
```bash
PORT=8000
UVICORN_HOST=0.0.0.0
UVICORN_WORKERS=2

JWT_SECRET_KEY=supersecretkey

DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres123
DB_NAME=books
```

**⚠️ IMPORTANTE:** 
- `DB_HOST` deve ser `db` (nome do serviço no docker-compose, não `localhost`)
- `DB_NAME` deve estar definido (ex: `books`)
- `DB_USER` deve estar definido (ex: `postgres`, `admin`, etc - não usar espaços ou caracteres especiais)
- Se você receber erros como "database does not exist" ou "password authentication failed", execute:

```bash
# Parar containers e remover volumes antigos (isso apaga todos os dados do banco!)
docker compose down -v

# Verifique seu arquivo .env e garanta que todas as variáveis estão corretas
# Especialmente: DB_USER, DB_PASSWORD, DB_NAME

# Subir novamente
docker compose up -d --build
```

**Nota sobre volumes:** O comando `docker compose down -v` remove TODOS os dados do PostgreSQL. Use apenas se estiver começando do zero ou em desenvolvimento.

2) Suba com compose:
```bash
docker compose up -d --build
```

- A API ficará acessível em `http://127.0.0.1:${PORT}` (padrão 8000)
- PostgreSQL será inicializado automaticamente com healthcheck
- Para parar: `docker compose down`

### Acessar o Banco de Dados Externamente

O PostgreSQL está exposto na porta `${DB_PORT}` (padrão 5432) e pode ser acessado de fora do Docker.

**1. Usando psql (linha de comando):**
```bash
psql -h localhost -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME}
```

Exemplo com as configurações padrão:
```bash
psql -h localhost -p 5432 -U postgres -d books
# Digite a senha quando solicitado
```

**2. Connection String (para ferramentas GUI como DBeaver, pgAdmin, TablePlus, etc):**
```
Host: localhost
Port: ${DB_PORT} (padrão: 5432)
Database: ${DB_NAME}
Username: ${DB_USER}
Password: ${DB_PASSWORD}
```

**3. URL de conexão:**
```
postgresql://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}
```

**4. Usando docker exec (direto no container):**
```bash
docker exec -it m1-ml-book-flow-db psql -U ${DB_USER} -d ${DB_NAME}
```

**Exemplo completo:**
Se seu `.env` tiver:
```
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres123
DB_NAME=books
```

Então conecte com:
```bash
psql -h localhost -p 5432 -U postgres -d books
# Senha: postgres123
```

**⚠️ Problema de Autenticação no DBeaver/pgAdmin?**

Se você receber erro "password authentication failed", o volume do PostgreSQL pode ter sido criado com credenciais diferentes. Solução:

1. **Parar e remover o volume antigo:**
```bash
docker compose down -v
```

2. **Verificar seu `.env` e garantir que tenha:**
```
DB_USER=postgres
DB_PASSWORD=postgres123
DB_NAME=books
DB_PORT=5432
```

3. **Subir novamente:**
```bash
docker compose up -d
```

4. **Aguarde alguns segundos para o PostgreSQL inicializar completamente**

5. **Tente conectar novamente no DBeaver com:**
   - Host: `localhost`
   - Port: `5432` (ou o valor de `DB_PORT`)
   - Database: `books` (ou o valor de `DB_NAME`)
   - Username: `postgres` (ou o valor de `DB_USER`)
   - Password: `postgres123` (ou o valor de `DB_PASSWORD`)

**📝 Nota:** O comando `docker compose down -v` **APAGA TODOS OS DADOS** do banco. Use apenas se estiver OK em perder os dados ou se estiver em desenvolvimento.

**🔍 Verificar credenciais atuais do container:**
```bash
docker exec m1-ml-book-flow-db printenv | grep POSTGRES
```

### Endpoint de Scraping

O endpoint `/api/v1/scraping/trigger` permite fazer web scraping do site [books.toscrape.com](https://books.toscrape.com/) e armazenar os dados no PostgreSQL.

**Características:**
- Captura: título, preço, rating, disponibilidade, categoria, imagem e autor
- Armazena automaticamente no banco PostgreSQL
- Requer autenticação (Bearer token)
- Atualiza livros existentes ou cria novos

**Exemplo de uso:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/scraping/trigger \
  -H "Authorization: Bearer <seu_token>"
```

**Resposta:**
```json
{
  "message": "Scraping concluído com sucesso",
  "scraped_count": 1000,
  "saved_count": 1000
}
```
