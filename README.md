[![CI](https://github.com/aga87/garden-tasks-api/actions/workflows/ci.yml/badge.svg)](https://github.com/aga87/garden-tasks-api/actions)

# Garden Tasks API

Backend API for a mobile-first interface to manage and view community garden tasks.

This is a small volunteer project for Creative Garden Wageningen, built to solve a real coordination problem around managing seasonal tasks.
 
The API reads from a shared Google Sheet and exposes a structured, mobile-friendly task view. The design intentionally keeps the system simple: all processing (parsing, filtering, sorting) happens in memory, which is sufficient for the current scale and avoids unnecessary infrastructure.

## Tech Stack

- FastAPI (Python backend)
- Google Sheets (source of truth, no database)
- Next.js (frontend)

## Local Development Setup

### Environment variables

For local development, copy `.env.example` and provide values.

### Run locally

```bash
pip install --group dev -e .
uvicorn garden_app.main:app --reload
```

Open:
- http://127.0.0.1:8000 (service info)
- http://127.0.0.1:8000/docs (interactive API docs)

### Running tests

```shell
pytest
```

Common development tasks are available via the Makefile.


## Production Setup

### Infrastructure

Enable Secret Manager:

```bash
gcloud services enable secretmanager.googleapis.com
```

### Environment configuration

In production, configuration is provided via environment variables and Google Cloud Secret Manager.

You can bootstrap secrets from your local `.env` using the provided script:

```bash
bash scripts/bootstrap-secrets.sh GOOGLE_SHEETS_API_KEY
```