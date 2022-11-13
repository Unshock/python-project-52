#Makefile

install:
	poetry install

build:
	poetry build

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

test:
	poetry run pytest

lint:
	poetry run flake8 task_manager

tl:
	poetry run pytest 
	poetry run flake8 task_manager
