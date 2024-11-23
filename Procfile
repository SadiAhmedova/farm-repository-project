web: DJANGO_SETTINGS_MODULE=farm_app.settings gunicorn farm_app.wsgi
release: python manage.py migrate
web: gunicorn farm_app.wsgi