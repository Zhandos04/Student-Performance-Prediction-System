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

# Проверка существования таблиц и вывод подробной информации
echo "Checking database schema..."
PGPASSWORD=$SQL_PASSWORD psql -h $SQL_HOST -U $SQL_USER -d $SQL_DATABASE -c "\dt" || echo "Could not list tables, database may be empty"

# Вывод всех команд для отладки
set -x

# Полная очистка и пересоздание миграций
echo "Recreating all migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Создание новых миграций для всех приложений 
python manage.py makemigrations accounts
python manage.py makemigrations dashboard
python manage.py makemigrations ml_model
python manage.py makemigrations

# Детальная информация о миграциях для отладки
python manage.py showmigrations

# Выполнение миграций в определённом порядке с подробным выводом
echo "Applying migrations with verbose output..."
python manage.py migrate auth --verbosity 3
python manage.py migrate contenttypes --verbosity 3
python manage.py migrate admin --verbosity 3
python manage.py migrate sessions --verbosity 3
python manage.py migrate accounts --verbosity 3
python manage.py migrate dashboard --verbosity 3
python manage.py migrate --verbosity 3

# Показываем структуру таблиц после миграции
echo "Checking tables after migrations..."
PGPASSWORD=$SQL_PASSWORD psql -h $SQL_HOST -U $SQL_USER -d $SQL_DATABASE -c "\dt"

# Собираем статические файлы
python manage.py collectstatic --no-input

# Создаем суперпользователя (только если он не существует)
echo "Creating superuser if needed..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword123')"

# Обновляем библиотеки для ML-модели перед обучением
echo "Updating ML libraries..."
pip install --upgrade numpy pandas scikit-learn matplotlib seaborn

# Обучаем модель ML
echo "Training ML model..."
mkdir -p /app/ml_model/models
python manage.py train_ml_model || echo "ML model training failed, but continuing startup."

# Отключаем вывод всех команд
set +x

# Запускаем сервер
echo "Starting web server..."
exec "$@"