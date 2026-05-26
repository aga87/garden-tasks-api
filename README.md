[![CI](https://github.com/aga87/garden-tasks-api/actions/workflows/ci.yml/badge.svg)](https://github.com/aga87/garden-tasks-api/actions)

# Garden Tasks API

- FastAPI backend for a mobile-first community garden task management application
- Deployed and used in production to support real-world coordination of seasonal tasks
- Integrates with Google Sheets as the source of truth, avoiding the need for a dedicated database
- Applies in-memory transformations (parsing, filtering, sorting) to prepare task data for API responses
- Provides a structured API layer consumed by a Next.js frontend
- Designed with a focus on simplicity, low operational overhead, and fast iteration, avoiding premature optimisation

## Tech Stack

- Python
- FastAPI
- Google Sheets API
- Terraform
- Google Cloud Run
- GitHub Actions

## Environments

The project currently uses a single production environment to keep infrastructure simple and cost-effective. Changes are validated locally and through CI before deployment. A separate staging environment would be the next step if the project gains more users, higher risk, or more frequent releases.


## Local Development

### Prerequisites

Install:
1. Python. Python version requirements are defined in `pyproject.toml` (and `.python-version` if present). `uv` will automatically use or install a compatible version.
2. [Install uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation). It improves build and development environment setup speed
3. Docker (optional, for container-based development)
4. [Install Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk) - (`gcloud`) (required for local authentication)

### Local Development Setup

1. Copy `.env.example` to `.env` and provide values:

- `GARDEN_SHEET_ID` — Google Sheet ID from the spreadsheet URL
- `GARDEN_SHEET_RANGE` - Spreadsheet range in [A1 notation](https://developers.google.com/workspace/sheets/api/guides/concepts#a1-notation) covering the task table (e.g. `A1:C3`) 


3. Authenticate locally:

```bash
gcloud auth application-default login
```

4. Install dependencies and create the virtual environment:

```bash
uv sync
```

### Running the application

Run the app with 

```bash
uv run uvicorn garden_app.main:app --reload
``` 

or 

```bash
make run
```

Open:

- http://127.0.0.1:8000 (service info)
- http://127.0.0.1:8000/docs (interactive API docs)

### Running tests

```shell
pytest
```

Common development tasks are available via the Makefile.


## Docker

```shell
docker build -t creative-garden-api .
docker run --env-file .env -p 8080:8080 garden-tasks-api
```


## Infrastructure (Terraform)

Infrastructure is provisioned using Terraform.

### Prerequisites

1. [Install Terraform](https://developer.hashicorp.com/terraform/install)

2. [Install TFLint](https://github.com/terraform-linters/tflint?utm_source=chatgpt.com)

3. [Install TFSec](https://aquasecurity.github.io/tfsec/v0.63.1/getting-started/installation/)


### Configuration

Terraform environment configuration lives in:

```text
infra/prod.tfvars
```

### Workflow

Terraform workflow commands are defined in `infra/Makefile`, including formatting, validation, linting, planning, and applying changes.

```bash
cd infra

terraform init # one-off

make plan
make apply
make destroy
```

Commands currently default to the production environment, configured through the `ENV ?= prod` setting in the Makefile. If a staging environment is added in the future, the default should be changed to `staging`.

## One-off Infrastructure Setup (GCP)

### 1. GitHub Actions Authentication (OIDC) with Google Cloud

Deployments are handled automatically via GitHub Actions.

GitHub Actions authenticates to GCP using Workload Identity Federation (OIDC) instead of long-lived JSON service account keys.

Terraform provisions:

- a dedicated GitHub Actions deployer service account
- a Workload Identity Pool
- a GitHub OIDC provider
- IAM bindings allowing the repository to impersonate the deployer service account

After applying Terraform, add the two GitHub secrets from Terraform outputs.

In GitHub, go to:
**Repository → Settings → Secrets and variables → Actions**

Create:

- `GCP_WORKLOAD_IDENTITY_PROVIDER` = `github_workload_identity_provider`
- `GCP_SERVICE_ACCOUNT` = `github_deployer_service_account_email`

### 2. Authenticate Docker with Artifact Registry

```shell
gcloud auth configure-docker <REGION>-docker.pkg.dev
```

Example:

```shell
gcloud auth configure-docker europe-west3-docker.pkg.dev
```

### 3. Google Sheets Authentication

The application uses Google Application Default Credentials (ADC) for Google Sheets access.

In production, ADC resolves to the Cloud Run runtime service account provisioned by Terraform. Share the spreadsheet with the service account email from the Terraform output:

```shell
terraform output cloud_run_runtime_service_account_email
```

Grant Viewer access unless the API needs to write to the sheet.

For local development, authenticate with ADC using service account impersonation:

First grant your Google user permission to impersonate the runtime service account:

```shell
gcloud iam service-accounts add-iam-policy-binding \
  "$(terraform output -raw cloud_run_runtime_service_account_email)" \
  --member="user:YOUR_EMAIL@gmail.com" \
  --role="roles/iam.serviceAccountTokenCreator" \
  --project="$(terraform output -raw project_id)"
```

Then authenticate local ADC:

```shell
gcloud auth application-default login \
  --impersonate-service-account="$(terraform output -raw cloud_run_runtime_service_account_email)"
```

This lets local development use the same service account as Cloud Run. Your Google user must be allowed to impersonate the service account.

### 4. Environment configuration

In production, configuration is provided via environment variables:

- `GARDEN_SHEET_ID`
- `GARDEN_SHEET_RANGE`

## Deployment

This service is deployed to Cloud Run via GitHub Actions on pushes to `main`.

The workflow:

1. Authenticates to Google Cloud using GitHub OIDC
2. Builds the Docker image for linux/amd64
3. Pushes the image to Artifact Registry
4. Deploys the image to Cloud Run

See: `.github/workflows/deploy.yml`
