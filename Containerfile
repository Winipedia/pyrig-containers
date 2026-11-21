FROM python:3.15-slim
WORKDIR /pyrig-containers

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY LICENSE README.md pyproject.toml uv.lock ./
COPY src/pyrig_containers src/pyrig_containers

RUN uv sync --no-group=dev

RUN useradd --create-home --uid=1000 appuser && chown appuser:appuser .
USER 1000

ENTRYPOINT ["uv", "run", "--no-sync", "pyrig-containers"]
