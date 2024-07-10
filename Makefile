dbshell:
	poetry run python manage.py dbshell

shell:
	poetry run python manage.py shell

createsuperuser:
	poetry run python manage.py createsuperuser

translate:
	poetry run django-admin makemessages --ignore="static" --ignore=".env" -l ru

compilemessages:
	poetry run django-admin compilemessages

build:
	poetry install --extras psycopg2-binary
	poetry run python manage.py migrate

start-deploy:
	gunicorn task_manager.wsgi

install:
	poetry install

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

setup:
	cp -n .env.example .env || true
	make install
	make migrate

start:
	poetry run python manage.py runserver 127.0.0.1:8000

check:
	poetry check

lint:
	poetry run flake8 .

test:
	poetry run python manage.py test
