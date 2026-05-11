# Workload Identity Pool used for GitHub Actions authentication
resource "google_iam_workload_identity_pool" "github_actions" {
  project                   = var.project_id
  workload_identity_pool_id = "github-pool"
  display_name              = "GitHub Actions Pool"
  description               = "Workload Identity Pool for GitHub Actions"

  depends_on = [
    google_project_service.project_services["iam.googleapis.com"],
  ]
}

# GitHub OIDC provider used to authenticate GitHub Actions to GCP
resource "google_iam_workload_identity_pool_provider" "github_actions" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_actions.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Provider"
  attribute_condition                = "assertion.repository == '${var.github_repository}' && assertion.ref == 'refs/heads/${var.github_deploy_branch}'"

  attribute_mapping = {
    "google.subject"             = "assertion.sub"
    "attribute.actor"            = "assertion.actor"
    "attribute.ref"              = "assertion.ref"
    "attribute.repository"       = "assertion.repository"
    "attribute.repository_owner" = "assertion.repository_owner"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Allow GitHub Actions identities from this repository to impersonate the deployer service account
resource "google_service_account_iam_member" "github_deployer_workload_identity_user" {
  service_account_id = google_service_account.github_deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_actions.name}/attribute.repository/${var.github_repository}"
}
