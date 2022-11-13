#Makefile

install:
	poetry install

build:
	poetry build

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

test:
	poetry run pytest

dtest:
	python manage.py test

lint:
	poetry run flake8 task_manager

tl:
	poetry run pytest 
	poetry run flake8 task_manager
