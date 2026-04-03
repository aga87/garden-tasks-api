#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="$(gcloud config get-value project 2>/dev/null)"

if [[ -z "$PROJECT_ID" ]]; then
  echo "No GCP project set. Run: gcloud config set project <PROJECT_ID>"
  exit 1
fi

ENV_FILE=".env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo ".env file not found"
  exit 1
fi

if [[ "$#" -eq 0 ]]; then
  echo "Usage: $0 SECRET_NAME [SECRET_NAME ...]"
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

upsert_secret() {
  local name="$1"
  local value="$2"

  if [[ -z "$value" ]]; then
    echo "Secret value for $name is empty or not set"
    exit 1
  fi

  if gcloud secrets describe "$name" --project="$PROJECT_ID" >/dev/null 2>&1; then
    printf '%s' "$value" | gcloud secrets versions add "$name" \
      --project="$PROJECT_ID" \
      --data-file=-
    echo "Updated secret version: $name"
  else
    printf '%s' "$value" | gcloud secrets create "$name" \
      --project="$PROJECT_ID" \
      --replication-policy="automatic" \
      --data-file=-
    echo "Created secret: $name"
  fi
}

for secret_name in "$@"; do
  secret_value="${!secret_name:-}"
  upsert_secret "$secret_name" "$secret_value"
done

echo "Secrets bootstrapped."

gcloud secrets list --project="$PROJECT_ID"