#Makefile

install:
	poetry install

build:
	poetry build

run:
	poetry run python manage.py runserver

wsgi_run:
	poetry run gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

test:
	poetry run pytest

lint:
	poetry run flake8 task_manager

tl:
	poetry run pytest 
	poetry run flake8 task_manager
