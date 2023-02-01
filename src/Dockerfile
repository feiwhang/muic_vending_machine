# base poetry env
FROM python:3.11.1-slim AS base

ENV POETRY_VERSION=1.3.2
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"


# builder poetry
FROM base AS builder
RUN apt-get update \
    && apt-get install --no-install-recommends --assume-yes curl
RUN curl -sSL https://install.python-poetry.org | python -


# run
FROM base AS runtime
COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY ../poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN poetry export --without-hashes -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt
WORKDIR /src/app
COPY ./src .
