ARG PROFILE="prod"
ARG BASE="slim-bookworm"

FROM python:3.12-${BASE} AS install-base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON=python3.12
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

FROM install-base AS install-prod

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM install-base AS install-dev

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --dev --no-install-project

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --dev

FROM install-${PROFILE} AS install

FROM install AS devcontainer

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y \
    less && \
    rm -rf /var/lib/apt/lists/*

FROM python:3.12-${BASE}

COPY --from=install --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
