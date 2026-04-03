[![CI](https://github.com/aga87/garden-tasks-api/actions/workflows/ci.yml/badge.svg)](https://github.com/aga87/garden-tasks-api/actions)

# Garden Tasks API

Backend API for a mobile-first interface to manage and view community garden tasks.

This is a small volunteer project for Creative Garden Wageningen, built to solve a real coordination problem around managing seasonal tasks.
 
The API reads from a shared Google Sheet and exposes a structured, mobile-friendly task view. The design intentionally keeps the system simple: all processing (parsing, filtering, sorting) happens in memory, which is sufficient for the current scale and avoids unnecessary infrastructure.

## Tech Stack

- FastAPI (Python backend)
- Google Sheets (source of truth, no database)
- Next.js (frontend)

___

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

**Build and run with Docker**

```shell
docker build -t creative-garden-api .
docker run --env-file .env -p 8080:8080 garden-tasks-api
```

### Running tests

```shell
pytest
```

Common development tasks are available via the Makefile.

___

## Production Setup

### One-off Infrastructure Setup

#### Enable Secret Manager and Cloud Run API:

```bash
gcloud services enable secretmanager.googleapis.com
gcloud services enable run.googleapis.com
```

#### Create service account:

```shell
gcloud iam service-accounts create SERVICE_ACCOUNT_NAME \
  --display-name="Display name"
```

Example: 

```shell
gcloud iam service-accounts create garden-tasks-api-sa \
  --display-name="Garden Tasks API Cloud Run Service"
```

#### Grant service account permissions to read secrets

```shell
# Command
gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member="serviceAccount:<SERVICE_ACCOUNT_NAME>@<PROJECT_ID>.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
 ```

Example: 

```shell 
gcloud projects add-iam-policy-binding garden-tasks-api \
  --member="serviceAccount:garden-tasks-api-sa@garden-tasks-api.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

#### Authenticate Docker with Artifact Registry

```shell
gcloud auth configure-docker <REGION>-docker.pkg.dev
```

Example:

```shell
gcloud auth configure-docker europe-west3-docker.pkg.dev
```

#### Create the Artifact Registry repository

```shell
gcloud artifacts repositories create <REPOSITORY_NAME> \
--project=<PROJECT_ID> \
--repository-format=docker \
--location=<REGION> \
--description="Docker repository for <DESCRIPTION>"
```

Example:

```shell
gcloud artifacts repositories create garden-tasks-api-repo \
  --project=garden-tasks-api \
  --repository-format=docker \
  --location=europe-west3 \
  --description="Docker repository for Garden Tasks API"
```

#### Environment configuration

In production, configuration is provided via environment variables and Google Cloud Secret Manager.

You can bootstrap secrets from your local `.env` using the provided script:

```bash
bash scripts/bootstrap-secrets.sh GOOGLE_SHEETS_API_KEY
```

