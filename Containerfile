FROM python:3.15-slim
WORKDIR /pyrig-containers

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY LICENSE README.md pyproject.toml uv.lock ./
COPY src/pyrig_containers src/pyrig_containers

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1 UV_LOCKED=1 UV_NO_EDITABLE=1 UV_NO_GROUP=dev UV_NO_SYNC=1

RUN uv sync

RUN useradd --create-home --uid=1000 appuser \
    && chown appuser:appuser .
USER 1000

ENTRYPOINT ["uv", "run", "pyrig-containers"]
