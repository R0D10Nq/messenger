# My Messenger

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![React](https://img.shields.io/badge/React-18-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6)
![License](https://img.shields.io/badge/License-MIT-yellow)

Современный мессенджер с E2E шифрованием, голосовыми сообщениями, транскрипцией и групповыми чатами.

## Возможности

- **Аутентификация**: JWT + refresh tokens, 2FA (TOTP)
- **Чаты**: 1:1 и групповые с ролями (owner/admin/member)
- **Сообщения**: текст, статусы доставки/прочтения, редактирование, потоки/треды
- **Медиа**: изображения, видео, аудио, документы
- **Голосовые**: запись и воспроизведение, автотранскрипция
- **Звонки**: аудио/видео через WebRTC
- **E2E шифрование**: Signal Protocol (identity keys, prekeys)
- **Real-time**: WebSocket (typing indicator, статусы онлайн)
- **Реакции**: эмодзи-реакции на сообщения
- **Поиск**: полнотекстовый поиск по сообщениям и чатам
- **Уведомления**: гибкие настройки, тихие часы, отключение по чатам
- **Темы**: светлая/тёмная/системная тема, кастомные цвета
- **Модерация**: блокировка пользователей, жалобы
- **Самоудаляющиеся сообщения**: ephemeral messages с таймером

## Стек технологий

| Компонент | Технология |
|-----------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 |
| База данных | PostgreSQL 16 |
| Кеш/Pub-Sub | Redis 7 |
| Real-time | python-socketio |
| Frontend | React 18, TypeScript, Vite |
| Стилизация | Tailwind CSS |
| State | Zustand |
| Миграции | Alembic |

## Быстрый старт

### Docker Compose (рекомендуется)

```bash
cp .env.example .env
docker compose up -d
```

- Frontend: <http://localhost:3000>
- Backend API: <http://localhost:8000/api>
- API Docs: <http://localhost:8000/docs>

### Локальная разработка

#### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Linux: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
uvicorn src.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Тестирование

```bash
# Backend (86 тестов)
cd backend
pytest -v
mypy src/
ruff check .

# Frontend
cd frontend
npm test
npm run lint
```

## Структура проекта

```
my-messenger/
├── backend/
│   ├── alembic/           # Миграции БД
│   ├── src/
│   │   ├── api/           # REST эндпоинты
│   │   ├── models/        # SQLAlchemy модели
│   │   ├── schemas/       # Pydantic схемы
│   │   ├── services/      # Бизнес-логика
│   │   └── websocket/     # Socket.IO
│   └── tests/             # Pytest
├── frontend/
│   └── src/
│       ├── components/    # React компоненты
│       ├── hooks/         # Custom hooks
│       ├── pages/         # Страницы
│       ├── services/      # API клиенты
│       ├── store/         # Zustand stores
│       └── types/         # TypeScript типы
├── docker-compose.yml
└── .env.example
```

## API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| POST | /api/auth/register | Регистрация |
| POST | /api/auth/login | Вход |
| GET | /api/profile/me | Профиль |
| GET | /api/chats | Список чатов |
| POST | /api/chats/{id}/messages | Отправка сообщения |
| POST | /api/media/upload | Загрузка файла |
| POST | /api/2fa/setup | Настройка 2FA |
| POST | /api/calls | Инициация звонка |

Полная документация: <http://localhost:8000/docs>

## Переменные окружения

```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/messenger
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

## Лицензия

MIT
