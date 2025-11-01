# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Install Poetry via pip (no apt dependencies)
RUN pip install --no-cache-dir "poetry==1.8.3"

# Leverage Docker layer caching for dependencies
COPY pyproject.toml poetry.lock* ./

# Update lock file if needed and install prod dependencies
# poetry lock updates the lock file if pyproject.toml changed
RUN poetry lock --no-update || poetry lock \
    && poetry install --no-interaction --no-ansi --without dev --no-root \
    && pip install --no-cache-dir prometheus-fastapi-instrumentator==6.1.0

# Copy application code
COPY m1_ml_book_flow_api ./m1_ml_book_flow_api

# Copy dashboards directory for Streamlit
COPY dashboards ./dashboards

# Copy startup script
COPY start.sh ./start.sh
RUN chmod +x start.sh

EXPOSE 8000

# Use startup script for Heroku compatibility (single container)
CMD ["./start.sh"]


