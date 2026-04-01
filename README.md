[![CI](https://github.com/aga87/garden-tasks-api/actions/workflows/ci.yml/badge.svg)](https://github.com/aga87/garden-tasks-api/actions)

# Garden Tasks API

Backend API for a mobile-first interface to manage and view community garden tasks.

The API reads from a shared Google Sheet and exposes a clean, mobile-friendly task view.

## Tech Stack

- FastAPI (Python backend)
- Next.js (planned frontend)
- Google Sheets (source of truth)


## Run locally

```bash
pip install --group dev -e .
uvicorn garden_app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs
