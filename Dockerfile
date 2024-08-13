ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim-bullseye AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USERNAME=app
ENV USER_UID=1000
ENV USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}
USER ${USERNAME}
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

RUN mkdir -p /home/${USERNAME}/code
COPY pyproject.toml /home/${USERNAME}/code
COPY poetry.lock /home/${USERNAME}/code
COPY manage.py /home/${USERNAME}/code
COPY currency_converter /home/${USERNAME}/code/currency_converter
COPY entrypoint.sh /home/${USERNAME}/code/

RUN cd /home/${USERNAME}/code && \
    pip install --no-cache-dir poetry==1.8.3 && \
    poetry config virtualenvs.create true && \
    poetry install --only main --no-root --no-interaction

# RUN chmod +x /home/${USERNAME}/code/entrypoint.sh

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

CMD ["/home/app/code/entrypoint.sh"]
