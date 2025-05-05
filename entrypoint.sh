#!/bin/bash

# Ждем доступности базы данных
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Создаем миграции для всех приложений
python manage.py makemigrations accounts
python manage.py makemigrations dashboard

# Применяем миграции
python manage.py migrate

# Собираем статические файлы
python manage.py collectstatic --no-input

# Создаем только суперпользователя (админ)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword123')" | python manage.py shell

# Обучаем начальную модель ML
python manage.py train_ml_model

# Запускаем сервер
exec "$@"