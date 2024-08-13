# Currency Converter

## Requirements

The project requires [Python 3.12](https://www.python.org/downloads/release/python-3120/) or higher and the [Poetry](https://python-poetry.org/) package manager.

## Description

The project is a simple currency converter that uses the [Exchange Rates API](https://api.apilayer.com/exchangerates_data) to convert currencies. Each conversion transaction is stored in a SQLite database.

## Endpoints

Access the API documentation at `/docs`.

## Useful Python commands

### Installation

After installing poetry, install the project dependencies with:

```sh
poetry install --with ci,tests,development
```

Also, install `poetry-plugin-dotenv` to load environment variables from a `.env` file:

```sh
poetry self add poetry-plugin-dotenv
```

### Pre-commit hooks

The project is offering [pre-commit](https://pre-commit.com/) hooks, please install them via

```console
pre-commit install
```

### GitHub Actions

Each commit in the main branch will trigger a pipeline which will run unit tests and different linting tools.
When successful it will also containerize the application, finally its scans the docker image for vulnerabilities with [Trivy](https://aquasecurity.github.io/trivy/v0.49/).

### Migrate

To run the migrations, use:

```sh
poetry run task manage migrate
```

### Development

To run the application in development mode, use:

```sh
poetry run task manage runserver
```

You can, also, run the containerized application:

```sh
docker-compose up
```

### Testing

To run the tests, use:

```sh
poetry run task test
```
