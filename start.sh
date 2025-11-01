#!/bin/bash

# Script de inicialização para Heroku
# Roda API FastAPI e Streamlit no mesmo container

echo "🚀 Iniciando BookFlow API + Dashboard..."

# Inicia Streamlit em background
echo "📊 Iniciando Streamlit Dashboard..."
streamlit run /app/dashboards/api_dashboards.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false &

# Aguarda alguns segundos para o Streamlit inicializar
sleep 5

# Inicia a API FastAPI
echo "🔧 Iniciando FastAPI..."
exec poetry run uvicorn m1_ml_book_flow_api.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --workers 1