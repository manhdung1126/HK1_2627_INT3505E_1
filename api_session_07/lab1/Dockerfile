FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt ./
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN groupadd -r app && useradd -r -g app -d /app app

COPY --from=builder /opt/venv /opt/venv
COPY src ./src
COPY migrations ./migrations

ENV VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1

USER app
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "product_api.factory:create_app()"]
