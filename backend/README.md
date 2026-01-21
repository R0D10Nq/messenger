# My Messenger Backend

FastAPI backend для мессенджера.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Запуск

```bash
uvicorn src.main:app --reload
```

## Тесты

```bash
pytest
mypy src/
ruff check .
```
