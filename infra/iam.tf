# Runtime service account used by the application (Cloud Run runtime identity for Cloud SQL, Secret Manager, etc.)
resource "google_service_account" "cloud_run_runtime" {
  project      = var.project_id
  account_id   = "garden-tasks-api-sa"
  display_name = "Garden Tasks API Cloud Run Service"
}

resource "google_project_iam_member" "cloud_run_runtime_project_roles" {
  for_each = toset([
    "roles/secretmanager.secretAccessor",
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cloud_run_runtime.email}"
}

# GitHub Actions deployer service account
resource "google_service_account" "github_deployer" {
  project      = var.project_id
  account_id   = "github-deployer"
  display_name = "GitHub deployer"
}

resource "google_project_iam_member" "github_deployer_project_roles" {
  for_each = toset([
    "roles/artifactregistry.writer",
    "roles/iam.serviceAccountUser",
    "roles/run.admin",
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.github_deployer.email}"
}
