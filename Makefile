dbshell:
	poetry run python manage.py dbshell

shell:
	django-admin shell

requirements: poetry.lock
	poetry export -f requirements.txt -o requirements.txt

translate:
	django-admin makemessages --ignore="static" --ignore=".env"  -l ru

compilemessages:
	django-admin compilemessages

build:
	poetry install --extras psycopg2-binary
	poetry run python manage.py migrate

start-deploy:
	gunicorn task_manager.wsgi

compose-setup: compose-build compose-install

compose-build:
	docker-compose build

compose-install:
	docker-compose run app make install

compose-bash:
	docker-compose run app bash

compose:
	docker-compose up

compose-lint:
	docker-compose run app make lint

compose-test:
	docker-compose run app make test

install:
	poetry install

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

test-coverage:
	poetry run coverage run manage.py test python_django_blog
	poetry run coverage html
	poetry run coverage report