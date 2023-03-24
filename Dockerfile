FROM python:3.10.0-alpine

# Устанавливаем переменную окружения PYTHONUNBUFFERED для вывода в консоль без буферизации
ENV PYTHONUNBUFFERED=1

# Установка рабочей директории /app
WORKDIR /appp

# Копирование файлов приложения в контейнер
COPY main.py ./
COPY OGE/ ./OGE/
COPY EGE/ ./EGE/
COPY .env ./

# Установка зависимостей
RUN apk update && apk add --no-cache gcc musl-dev linux-headers && \
    pip install --no-cache-dir telebot python-dotenv && \
    apk del gcc musl-dev linux-headers

# Команда для запуска приложения
CMD ["python", "main.py"]