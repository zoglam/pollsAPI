Prepare
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username admin --email test@test.test
```
Test
```
python manage.py test polls_app.tests.RequestForQuestion -v 2
```
Run
```
python manage.py runserver
```