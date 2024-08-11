ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim-bullseye AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /code

WORKDIR /code

COPY pyproject.toml poetry.lock /code/
COPY manage.py /code
COPY manage.py /code

RUN pip install --no-cache-dir poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction

ARG SECRET_KEY

ENV SECRET_KEY=$SECRET_KEY
ENV DEBUG=False

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "currency_converter.asgi:application"]
