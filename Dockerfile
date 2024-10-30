# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем зависимости для WeasyPrint и других библиотек
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-dev \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    libgirepository1.0-dev \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Выполняем миграции и собираем статику
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Открываем порт для сервера
EXPOSE 8000

# Запуск сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
