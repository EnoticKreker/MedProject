# FastAPI MEDPROJECT

Тестовый проект на FastAPI с использованием паттерна Repository. Суть проекта заключается в модификации и управлении excel файлом с последующей выгрузкой. 

В проекте используется:
- FastAPI
- SqlAlchemy
- Postgres
- Alembic
- Docker

## Установка .env
перейти в backend и создать .env с содержимым
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=postgres
DB_ECHO=True

# Настройки приложения
PROJECT_NAME=Support API
VERSION=0.1.0
DEBUG=True
MAX_FILE_SIZE=10485760

# CORS настройки
CORS_ALLOWED_ORIGINS=http://0.0.0.0:8000,http://127.0.0.1:8000
```
перейти в frontend и создать .env с содержимым
```
VITE_API_BASE_URL=http://localhost:8000
```

## Старт с Docker
```
docker-compose up --build
```

### Перейти по адресу для просмотра документации
```
http://127.0.0.1:8000/docs
```

### Перейти по адресу главной страницы
```
http://127.0.0.1:5173
```
