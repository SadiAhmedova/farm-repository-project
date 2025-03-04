release: python manage.py migrate

web: gunicorn farm_app.wsgi --workers=1 --threads=2 --log-file -
