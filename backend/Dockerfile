# Используем Python 3.12
FROM python:3.12-slim

# Устанавливаем зависимости
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . /app

# Открываем порт FastAPI
EXPOSE 8000

# Команда для запуска
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
