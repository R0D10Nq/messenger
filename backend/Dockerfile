# Backend Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей и README (требуется hatchling)
COPY pyproject.toml README.md ./

# Установка pip и зависимостей
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# Копирование исходного кода
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Создание директории для медиа
RUN mkdir -p /app/media

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Порт
EXPOSE 8000

# Запуск
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
