FROM python:3.10.11-bullseye
COPY ./requirements.txt ./requirements.txt

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2.0

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /task_manager

COPY pyproject.toml poetry.lock ./

COPY . .

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN poetry run python manage.py migrate

EXPOSE 8000
CMD ["gunicorn", "task_manager.wsgi:application", "--bind", "0.0.0.0:8000"]


#