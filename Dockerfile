FROM python:3.10

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    postgresql-client

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN python -m venv /app/.env
RUN /app/.env/bin/pip install --upgrade pip
RUN /app/.env/bin/pip install -r requirements.txt

COPY . /app/

ENV PATH="/app/.env/bin:$PATH"

RUN /app/.env/bin/python manage.py collectstatic --noinput
RUN /app/.env/bin/python manage.py makemigrations

CMD ["gunicorn", "farm_app.wsgi:application", "--bind", "0.0.0.0:8000"]