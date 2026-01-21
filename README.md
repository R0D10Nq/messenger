# My Messenger

Современный мессенджер с поддержкой голосовых сообщений, транскрипции и групповых чатов.

## Стек технологий

### Backend

- **Python 3.12** + **FastAPI**
- **PostgreSQL 16** + **SQLAlchemy 2.0**
- **Redis** (кеш, pub/sub)
- **python-socketio** (real-time)

### Frontend

- **React 18** + **TypeScript**
- **Vite** (сборка)
- **Tailwind CSS** + **Radix UI**
- **Zustand** (state management)

## Быстрый старт

### Запуск Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn src.main:app --reload
```

### Запуск Frontend

```bash
cd frontend
npm install
npm run dev
```

## Тестирование

### Тесты Backend

```bash
cd backend
pytest
mypy src/
ruff check .
```

### Тесты Frontend

```bash
cd frontend
npm test
npm run lint
```

## Структура проекта

```text
my-messenger/
├── backend/
│   ├── src/
│   │   ├── api/          # API эндпоинты
│   │   ├── models/       # SQLAlchemy модели
│   │   ├── schemas/      # Pydantic схемы
│   │   └── services/     # Бизнес-логика
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/   # React компоненты
│       ├── stores/       # Zustand stores
│       └── api/          # API клиент
└── docs/
```

## Лицензия

MIT
