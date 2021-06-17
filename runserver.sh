#!/bin/bash

cd /app
export PYTHONPATH=/app;$PYTHONPATH


python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_test_data.json
echo "from django.contrib.auth import get_user_model; import os; User = get_user_model(); User.objects.create_superuser(os.environ['DJANGO_SUPERUSER_USERNAME'], os.environ['DJANGO_SUPERUSER_EMAIL'], os.environ['DJANGO_SUPERUSER_PASSWORD']);print('Superuser created')" | python manage.py shell
echo "Files inside /app:"
ls /app
python manage.py runserver 0.0.0.0:$PORT
