ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

# TODO: Run app as non-root user
COPY pyproject.toml poetry.lock /code/
COPY . /code
RUN pip install --no-cache-dir poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction && \
    chmod +x entrypoint.sh

# TODO: secrets should be passed on secret mounts. See https://docs.docker.com/build/building/secrets/
ARG SECRET_KEY
ARG EXCHANGE_RATE_API_KEY
ARG EXCHANGE_BASE_URL
ARG PORT
ARG DJANGO_SUPERUSER_PASSWORD
ARG DJANGO_SUPERUSER_USERNAME
ARG DJANGO_SUPERUSER_EMAIL

ENV DEBUG=False
ENV EXCHANGE_RATE_API_KEY=${EXCHANGE_RATE_API_KEY}
ENV EXCHANGE_BASE_URL=${EXCHANGE_BASE_URL}
ENV SECRET_KEY=${SECRET_KEY}
ENV PORT=${PORT}
ENV DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD}
ENV DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME}
ENV DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL}

EXPOSE ${PORT}

CMD ["/code/entrypoint.sh"]
