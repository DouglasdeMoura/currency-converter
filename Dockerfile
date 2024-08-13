ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /code

WORKDIR /code

# TODO: Run app as non-root user
RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction
COPY . /code
RUN chmod +x /code/entrypoint.sh

# TODO: secrets should be passed on secret mounts. See https://docs.docker.com/build/building/secrets/
ARG SECRET_KEY
ARG EXCHANGE_RATE_API_KEY
ARG EXCHANGE_BASE_URL

ENV DEBUG=False
ENV EXCHANGE_RATE_API_KEY=${EXCHANGE_RATE_API_KEY}
ENV EXCHANGE_BASE_URL=${EXCHANGE_BASE_URL}
ENV SECRET_KEY=${SECRET_KEY}

VOLUME [ "/data" ]

EXPOSE 8000
ENTRYPOINT ["/code/entrypoint.sh"]
