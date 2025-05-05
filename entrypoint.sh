#!/bin/bash

set -e  # Останавливаем выполнение скрипта при любой ошибке

echo "Waiting for PostgreSQL..."
# Проверка доступности PostgreSQL с помощью netcat
while ! nc -z db 5432; do
  echo "PostgreSQL not available yet - waiting 1 second..."
  sleep 1
done
echo "PostgreSQL started successfully"

echo "Creating migrations for all apps if needed..."
# Сначала создаем миграции для всех приложений, если они отсутствуют
python manage.py makemigrations authentication
python manage.py makemigrations dashboard
python manage.py makemigrations notification
python manage.py makemigrations settings
python manage.py makemigrations support

echo "Running migrations in proper order..."
# Применяем миграции в правильном порядке
# Сначала базовые миграции Django
python manage.py migrate auth --noinput
python manage.py migrate contenttypes --noinput
python manage.py migrate sessions --noinput

# Затем миграции нашего приложения аутентификации
python manage.py migrate authentication --noinput

# Затем миграции для админки (которая зависит от custom user model)
python manage.py migrate admin --noinput

# Затем миграции для остальных наших приложений
python manage.py migrate dashboard --noinput
python manage.py migrate notification --noinput
python manage.py migrate settings --noinput
python manage.py migrate support --noinput

# В конце применяем все оставшиеся миграции для безопасности
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating initial data and superuser..."
python manage.py init_db

echo "Training ML models..."
python manage.py create_ml_models

echo "Starting server..."
exec gunicorn student_performance.wsgi:application --bind 0.0.0.0:8000