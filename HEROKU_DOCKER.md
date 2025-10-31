# Deploy no Heroku usando Docker

Este guia explica como fazer deploy da BookFlow API no Heroku usando containers Docker.

## 📋 Pré-requisitos

- Conta no Heroku
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) instalado
- Docker instalado localmente (opcional, para testes)
- Git configurado

## 🐳 Arquivos Configurados

### ✅ Necessários para Docker no Heroku:

#### `heroku.yml`
Instrui o Heroku a usar Docker para build e deploy via GitHub

#### `Dockerfile`
Dockerfile otimizado que:
- Usa Python 3.11-slim
- Instala dependências via Poetry
- Funciona tanto no Heroku quanto localmente
- Usa porta dinâmica `$PORT` (fornecida pelo Heroku)

#### `database.py`
Configurado para usar `DATABASE_URL` do Heroku automaticamente

### ❌ NÃO necessários com Docker:

- `Procfile` - Substituído pelo heroku.yml
- `runtime.txt` - Python definido no Dockerfile
- `requirements.txt` - Dependências instaladas via Poetry no Dockerfile

## 🚀 Deploy via GitHub (Automático) - RECOMENDADO

O `heroku.yml` permite deploy automático via GitHub usando Docker! 🎉

### Fluxo:
```
GitHub (push) → Heroku detecta heroku.yml → Build Docker → Deploy automático
```

### 1. Configurar Deploy Automático no Dashboard

**Opção A: Via Dashboard (Mais Fácil)**

1. Acesse o dashboard do seu app no Heroku
2. Vá em **Deploy** → **Deployment method** → Selecione **GitHub**
3. Conecte seu repositório GitHub
4. Escolha a branch (ex: `main`)
5. Ative **Enable Automatic Deploys** (opcional, mas recomendado)
6. Em **Settings**, verifique se o Stack está como **container**

**Opção B: Via CLI**

```bash
# Login no Heroku
heroku login

# Definir stack como container
heroku stack:set container -a seu-app-name

# Verificar stack
heroku stack -a seu-app-name
```

### 2. Adicionar PostgreSQL

No **dashboard do Heroku**:
- Vá em **Resources** → **Add-ons**
- Busque "**Heroku Postgres**"
- Selecione o plano (Essential-0 é o básico)

Ou via CLI:
```bash
heroku addons:create heroku-postgresql:essential-0 -a seu-app-name
```

### 3. Configurar Variáveis de Ambiente

No **dashboard** em **Settings** → **Config Vars**, adicione:

```
JWT_SECRET_KEY = [sua-chave-secreta]
JWT_ALGORITHM = HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
LOG_LEVEL = INFO
```

Ou via CLI:
```bash
heroku config:set JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" -a seu-app-name
heroku config:set JWT_ALGORITHM=HS256 -a seu-app-name
heroku config:set LOG_LEVEL=INFO -a seu-app-name
```

### 4. Commit e Push no GitHub

```bash
git add Dockerfile heroku.yml m1_ml_book_flow_api/core/database.py
git commit -m "Add Heroku Docker configuration"
git push origin main
```

**🎉 Pronto!** O Heroku vai:
- Detectar o push no GitHub automaticamente
- Ler o `heroku.yml` 
- Fazer build da imagem Docker
- Fazer deploy do container

Tudo automático! Cada push na branch configurada vai gerar um novo deploy.

## 🔧 Deploy Manual via Container Registry (Opcional)

Se preferir fazer push direto da imagem Docker:

### 1. Login no Container Registry

```bash
heroku container:login
```

### 2. Build e Push da Imagem

```bash
# Build e push em um comando
heroku container:push web -a seu-app-name

# Ou build local primeiro
docker build -t registry.heroku.com/seu-app-name/web .
docker push registry.heroku.com/seu-app-name/web
```

### 3. Release da Imagem

```bash
heroku container:release web -a seu-app-name
```

## 🧪 Testar Localmente com Docker

Antes de fazer deploy, teste localmente:

### 1. Criar arquivo `.env` local

```bash
cat > .env << EOF
DATABASE_URL=postgresql://user:pass@localhost:5432/books
JWT_SECRET_KEY=sua-chave-para-teste
JWT_ALGORITHM=HS256
PORT=8000
EOF
```

### 2. Build da Imagem

```bash
docker build -t bookflow-api .
```

### 3. Rodar Container

```bash
# Com PostgreSQL local
docker run -p 8000:8000 --env-file .env bookflow-api

# Ou usando docker-compose (se tiver)
docker-compose up
```

Acesse: http://localhost:8000/docs

## 📊 Monitoramento

### Ver Logs

```bash
# Logs em tempo real
heroku logs --tail -a seu-app-name

# Últimas 1000 linhas
heroku logs -n 1000 -a seu-app-name

# Filtrar por tipo
heroku logs --source app --tail -a seu-app-name
```

### Informações do Container

```bash
# Ver status
heroku ps -a seu-app-name

# Ver tipo de dyno
heroku ps:type -a seu-app-name

# Restart do container
heroku restart -a seu-app-name
```

### Banco de Dados

```bash
# Informações do PostgreSQL
heroku pg:info -a seu-app-name

# Conectar ao banco
heroku pg:psql -a seu-app-name

# Ver DATABASE_URL
heroku config:get DATABASE_URL -a seu-app-name
```

## 🔍 Verificação Pós-Deploy

1. **API Docs**: `https://seu-app.herokuapp.com/docs`
2. **Health Check**: `https://seu-app.herokuapp.com/api/v1/health`
3. **Métricas**: `https://seu-app.herokuapp.com/metrics`

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs de build
heroku builds -a seu-app-name

# Ver logs de runtime
heroku logs --tail -a seu-app-name

# Verificar se é container stack
heroku stack -a seu-app-name
```

### Erro de conexão com banco

```bash
# Verificar DATABASE_URL
heroku config:get DATABASE_URL -a seu-app-name

# Testar conexão
heroku pg:psql -a seu-app-name -c "SELECT 1"

# Ver credenciais do banco
heroku pg:credentials:url -a seu-app-name
```

### Build lento

O Heroku faz cache das layers do Docker, mas se quiser forçar rebuild:

```bash
# Via Container Registry
heroku container:push web --arg NO_CACHE=true -a seu-app-name

# Via GitHub (commit vazio)
git commit --allow-empty -m "Force rebuild"
git push origin main
```

## 📈 Otimizações

### Multi-stage Build

Para imagens menores, considere multi-stage builds no Dockerfile:

```dockerfile
FROM python:3.11-slim AS builder
# ... instalar dependências

FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# ... resto da aplicação
```

### Health Checks

Adicione ao `heroku.yml`:

```yaml
build:
  docker:
    web: Dockerfile
run:
  web: uvicorn m1_ml_book_flow_api.main:app --host 0.0.0.0 --port $PORT --workers 2
```

## 🔒 Segurança

- ✅ Nunca commite `.env` ou secrets
- ✅ Use `Config Vars` do Heroku para secrets
- ✅ Mantenha imagens atualizadas
- ✅ Use HTTPS (automático no Heroku)

## 📚 Recursos

- [Heroku Container Registry](https://devcenter.heroku.com/articles/container-registry-and-runtime)
- [heroku.yml Reference](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## ✅ Vantagens do Docker no Heroku

- 🐳 Ambiente idêntico entre dev e produção
- 📦 Controle total sobre dependências
- 🚀 Build mais rápido com cache de layers
- 🔧 Facilita debug (mesma imagem localmente)
- 📊 Melhor para workloads específicos

---

**Desenvolvido para o Projeto da Pós Tech em Machine Learning da FIAP**

