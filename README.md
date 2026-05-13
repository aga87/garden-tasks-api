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

## Infrastructure (Terraform)

Infrastructure is provisioned using Terraform.

### Prerequisites

1. Install [Terraform](https://developer.hashicorp.com/terraform/install)
2. Install TFLint

```bash
# macOS
brew install tflint

# Windows (install Chocolatey first)
choco install tflint
```

3. Install TFSec

```bash
# macOS
brew install 

# Windows
choco install tfsec
```

4. (Windows-only) Install make

```powershell
choco install make
```

### Configuration

Create environment variable files for each Terraform environment:

```bash
# cp infra/staging.tfvars.example infra/staging.tfvars
cp infra/prod.tfvars.example infra/prod.tfvars
```

### Workflow

Terraform workflow commands are defined in `infra/Makefile`, including formatting, validation, linting, planning, and applying changes.

```bash
cd infra

terraform init # one-off

make plan-prod
make apply-prod
make destroy-prod
```


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


## Local Development Setup

For local development, copy and rename `.env.example` to `.env` and provide values:

- GARDEN_SHEET_ID - from sheet URL (see details in the [mini-guide](https://knowsheets.com/how-to-get-the-id-of-a-google-sheet/))
- GARDEN_SHEET_RANGE - top-left to bottom-right cell of the tasks table (e.g., A1:C3) [developers.google](https://developers.google.com/workspace/sheets/api/guides/concepts#a1-notation)

### Python

1. Install [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation) as recommended on the home page. It improves build and development environment setup speed.
2. Clone repo to local machine, then from local repo's root execute in a shell `uv sync`, then on Windows `.venv/Scripts/activate` or UNIX `source .venv/bin/activate`

Now run the app with:

```shell
uvicorn garden_app.main:app --reload
```

Open:
- http://127.0.0.1:8000 (service info)
- http://127.0.0.1:8000/docs (interactive API docs)

## Docker

```shell
docker build -t creative-garden-api .
docker run --env-file .env -p 8080:8080 garden-tasks-api
```

### Running tests

```shell
pytest
```

Common development tasks are available via the Makefile.
