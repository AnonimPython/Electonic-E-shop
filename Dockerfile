# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Собираем статические файлы (нужно для production)
RUN python manage.py collectstatic --noinput

# Команда для запуска (будет переопределена в docker-compose для разработки)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]