# API

The API service is build using Python+FASTAPI

## Setup

### Install Poetry

Poetry is a tool for dependency management and packaging in Python.

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

Follow the instructions on how to add it to PATH.

### Set the path of virtual environment inside the project

```shell
poetry config virtualenvs.in-project true
```

### Install dependencies

Run the following command in terminal

```shell
poetry install
```

### Run the app in Development mode

Run the following command in terminal

```shell
poetry run uvicorn es.main:app --reload --host localhost --port 3100
```
