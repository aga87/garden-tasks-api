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

## Production setup (one-off)

### I. GCP Infrastructure Setup

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

### II. Environment configuration

In production, configuration is provided via environment variables and Google Cloud Secret Manager.

You can bootstrap secrets from your local `.env` using the provided script:

```bash
bash scripts/bootstrap-secrets.sh GOOGLE_SHEETS_API_KEY
```

### III. GitHub Actions authentication with Google Cloud

#### **1. Make sure the required APIs are enabled**


Workload Identity Federation relies on IAM and Security Token Service components:

```shell
gcloud services enable \
  iamcredentials.googleapis.com \
  sts.googleapis.com \
  iam.googleapis.com
```

#### **2. Set a few shell variables**


```shell
export PROJECT_ID="your-gcp-project-id" # Update this
export PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"

export GITHUB_ORG="your-github-username-or-org" # Update this
export REPO_NAME="your-repo-name" # Update this

# This is simply the **name of the Workload Identity Pool** you are about to create in GCP. Can copy as is. 
export POOL_ID="github-pool"
export PROVIDER_ID="github-provider" # Can copy as is 
export SERVICE_ACCOUNT_ID="github-deployer" # Copy as is, see the note below
```

#### **3. Create the service account**

```shell
gcloud iam service-accounts create "$SERVICE_ACCOUNT_ID" \
  --project="$PROJECT_ID" \
  --display-name="GitHub deployer"
```

Its email will be:

```shell
export SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_ID}@${PROJECT_ID}.iam.gserviceaccount.com"
echo "$SERVICE_ACCOUNT_EMAIL"
```

This email is what you will save in GitHub as `GCP_SERVICE_ACCOUNT`. 

#### **4. Grant that service account the roles it needs**

```shell
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/artifactregistry.writer"
```

```shell
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/iam.serviceAccountUser"
```

#### **5. Create the Workload Identity Pool**

```bash
gcloud iam workload-identity-pools create "$POOL_ID" \
  --project="$PROJECT_ID" \
  --location="global" \
  --display-name="GitHub Actions Pool"
```

This pool is the container for identities coming from GitHub Actions. 


#### **6. Create the GitHub OIDC provider inside that pool**
 
```shell
gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_ID" \
  --project="$PROJECT_ID" \
  --location="global" \
  --workload-identity-pool="$POOL_ID" \
  --display-name="GitHub Provider" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner,attribute.ref=assertion.ref" \
  --attribute-condition="assertion.repository=='${GITHUB_ORG}/${REPO_NAME}' && assertion.ref=='refs/heads/main'"
```

- This means only tokens from that exact repository **and** the main branch will satisfy the provider condition.
  

#### **7. Allow identities from that repo to impersonate the service account**

This grants principals from that Workload Identity Pool, limited to your repository, the ability to act as the service account. For the service-account-based setup, `roles/iam.workloadIdentityUser` is required. 

```shell
gcloud iam service-accounts add-iam-policy-binding "$SERVICE_ACCOUNT_EMAIL" \
  --project="$PROJECT_ID" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${GITHUB_ORG}/${REPO_NAME}"
```

#### **8. Get the exact provider resource name**

```shell
gcloud iam workload-identity-pools providers describe "$PROVIDER_ID" \
  --project="$PROJECT_ID" \
  --location="global" \
  --workload-identity-pool="$POOL_ID" \
  --format="value(name)"
```

It will output something like:

```
projects/123456789/locations/global/workloadIdentityPools/github-pool/providers/github-provider
```

That exact string is your:

```
GCP_WORKLOAD_IDENTITY_PROVIDER
```

This is the value your GitHub workflow uses. 

  
#### **9. Add the two GitHub secrets**

In GitHub, go to:
**Repository → Settings → Secrets and variables → Actions**

Create:

- `GCP_WORKLOAD_IDENTITY_PROVIDER` = the full provider resource name from step 8
- `GCP_SERVICE_ACCOUNT` = the service account email from step 3

Those are the exact two values used by the auth action. 

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
