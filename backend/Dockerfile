FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set environment variables for optimization
ENV CONTAINER_HOME=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV UV_LINK_MODE=copy
ENV PATH="${CONTAINER_HOME}/.venv/bin:$PATH"

WORKDIR $CONTAINER_HOME

# Install only essential system dependencies for web API
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/* && \
    rm -rf /tmp/*

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY app ./app

CMD ["sh", "-c", "uv run app/api/generate_tables.py && uvicorn app.api.main:app --host 0.0.0.0 --port 8000"]
