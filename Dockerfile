FROM python:3.12 AS poetry

ENV PATH "/root/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_IN_PROJECT 1

WORKDIR /root
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install curl -y --no-install-recommends && \
    curl -sSL https://install.python-poetry.org | python -
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main,docker


FROM python:3.12-slim AS base

ENV PYTHONPATH "/app"


WORKDIR /app

RUN groupadd -g 5000 container && useradd -d /app -m -g container -u 5000 container

COPY --from=poetry /root/.venv ./.venv
COPY . .

FROM base AS final

RUN chown -R 5000:5000 /app
USER container

CMD [".venv/bin/dumb-init", ".venv/bin/python", "src"]
