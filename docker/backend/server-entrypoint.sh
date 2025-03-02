#!/bin/sh

until cd /app/backend
do
    echo "Waiting for Django application (server volume)..."
done

until python manage.py makemigrations && python manage.py migrate
do
    echo "Waiting for database..."
    sleep 2
done

echo "Collecting static files..."
python manage.py collectstatic --noinput

# python manage.py createsuperuser --noinput

#exec gunicorn --reload DjangoCore.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4 --> will be needed for multithreading

# for debug
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
