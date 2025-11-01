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
COPY dashboards ./dashboards

EXPOSE 8000

# Require environment variables to be set by the runtime (.env via compose)
CMD ["sh", "-c", ": \"${PORT?Missing PORT}\"; : \"${UVICORN_HOST?Missing UVICORN_HOST}\"; : \"${UVICORN_WORKERS?Missing UVICORN_WORKERS}\"; : \"${JWT_SECRET_KEY?Missing JWT_SECRET_KEY}\"; uvicorn m1_ml_book_flow_api.main:app --host \"$UVICORN_HOST\" --port \"$PORT\" --workers \"$UVICORN_WORKERS\""]


