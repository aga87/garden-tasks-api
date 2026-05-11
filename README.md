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
```

3. Install TFSec

```bash
# macOS
brew install tfsec
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

### Ib. GCP Infrastructure Setup - Google OAuth2 Service Account Authentication

1. Create service account

```shell
gcloud iam service-accounts create garden-sheet-reader \
  --display-name="Garden Sheets Reader"
```

Get the email:

```shell
gcloud iam service-accounts list --filter="email:garden-sheet-reader"
```


2. Create JSON key

```shell
gcloud iam service-accounts keys create ./service-account-key.json \
  --iam-account=garden-sheet-reader@garden-tasks-api.iam.gserviceaccount.com 
```

3. Save the key to Secret Manager

4. Share the spreadsheet with this service account


### II. Environment configuration

In production, configuration is provided via environment variables and Google Cloud Secret Manager.

You can bootstrap secrets from your local `.env` using the provided script:

```bash
bash scripts/bootstrap-secrets.sh GOOGLE_SERVICE_ACCOUNT_JSON
```




___


## Deployment

### First deployment (manual)

#### 1. Build the image locally - M1/M2 Mac

```shell
docker buildx build --platform linux/amd64 -t <LOCAL_IMAGE_NAME> <BUILD_CONTEXT>
```

Example

```shell
docker buildx build --platform linux/amd64 -t garden-tasks-api .
```

#### 2. Tag the Image for Artifact Registry

```shell
docker tag <LOCAL_IMAGE_NAME> <REGION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY_NAME>/<REMOTE_IMAGE_NAME>
```
Example:

```shell
docker tag garden-tasks-api europe-west3-docker.pkg.dev/garden-tasks-api/garden-tasks-api-repo/garden-tasks-api
```

#### 3. Push to Artifact Registry

```shell
docker push <REGION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY_NAME>/pdf-processing-service
```

Example

```shell
docker push europe-west3-docker.pkg.dev/garden-tasks-api/garden-tasks-api-repo/garden-tasks-api
```

#### 4. Deploy to Cloud Run

**First deployment**

```shell
gcloud run deploy garden-tasks-api \
  --image europe-west3-docker.pkg.dev/YOUR_PROJECT_ID/garden-tasks-api-repo/garden-tasks-api \
  --region europe-west3 \
  --service-account=garden-tasks-api-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --concurrency=1 \
  --max-instances=1 \
  --allow-unauthenticated \
  --set-env-vars "KEY=VALUE" \
  --update-secrets "SECRET_ENV_VAR=SECRET_NAME:latest"
```

Example

```shell
gcloud run deploy garden-tasks-api \
  --image europe-west3-docker.pkg.dev/garden-tasks-api/garden-tasks-api-repo/garden-tasks-api \
  --region europe-west3 \
  --service-account=garden-tasks-api-sa@garden-tasks-api.iam.gserviceaccount.com \
  --concurrency=1 \
  --max-instances=1 \
  --allow-unauthenticated \
   --set-env-vars "GARDEN_SHEET_ID=1mL8fGL-NH3Ee3A7HnteAQ6JOl1xE7Mk5lCUFceVCQJg,GARDEN_SHEET_RANGE=Yearly tasks" \
  --update-secrets "GOOGLE_SERVICE_ACCOUNT_JSON=GOOGLE_SERVICE_ACCOUNT_JSON:latest"
```

### Subsequent deployments

This service is deployed to Cloud Run via GitHub Actions on pushes to main.

The workflow: 
1. Authenticates to Google Cloud using GitHub OIDC 
2. Builds the Docker image for linux/amd64 
3. Pushes the image to Artifact Registry 
4. Deploys the image to Cloud Run

See: `.github/workflows/deploy.yml`


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
