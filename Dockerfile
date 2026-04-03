FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir .

CMD ["sh", "-c", "uvicorn garden_app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]