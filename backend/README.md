## Старт без Docker
### Virtualenv
```
python -m venv venv
```
- Linux / MacOS
```
venv/bin/activate
```
- Windows
```
python venv\Scripts\activate
```

### Установка зависимостей
```
pip install -r requirements.txt
```

### База данных
В файл `.env` прописать свои настройки Postgres

Пример для back:
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

### Alembic migrate
```
alembic upgrade head
```

### Старт
```
python main.py
```

### Перейти по адресу
```
http://localhost:8000/docs
```
