# Blogging Platform

## Prerequisites

- Docker
- Python

## Local development setup

1. docker compose up -d

2. source ./venv/bin/activate

3. python manage.py migrate

3. python manage.py runserver


The following UIs are exposed:
- localhost:8000 - Blogging Platform
- localhost:8000/admin - Django Admin Console
- localhost:8080 - adminer PostgreSQL GUI