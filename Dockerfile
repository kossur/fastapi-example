FROM python:3.11.2-slim as python-base

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV GIT_VERSION="${GIT_VERSION}"

# python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# pip
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

# poetry
ENV POETRY_VERSION=1.4.0
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

ENV PYSETUP_PATH="/opt/pysetup"
ENV VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as build-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

RUN curl -sSL https://install.python-poetry.org | python

WORKDIR $PYSETUP_PATH
COPY pyproject.toml ./

RUN poetry install


FROM python-base as development
ENV APP_ENV=development
WORKDIR $PYSETUP_PATH

COPY --from=build-base $POETRY_HOME $POETRY_HOME
COPY --from=build-base $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install --with dev

WORKDIR /app

EXPOSE 8000
COPY ./app .

CMD [ "uvicorn", "main:app", "--proxy-header", "--host", "0.0.0.0", "--port", "8000" ]
