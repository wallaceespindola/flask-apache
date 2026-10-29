FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN uv venv /opt/venv && VIRTUAL_ENV=/opt/venv uv pip install --no-cache .

FROM python:3.14-slim AS runtime
LABEL org.opencontainers.image.authors="Wallace Espindola <wallace.espindola@gmail.com>" \
      org.opencontainers.image.source="https://github.com/wallaceespindola/flask-apache"
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN useradd --system --no-create-home app
USER app
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "flask_apache:create_app()"]
