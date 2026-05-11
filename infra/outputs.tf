output "project_id" {
  description = "GCP project ID."
  value       = var.project_id
}

output "cloud_run_runtime_service_account_email" {
  description = "Service account email to share the Google Sheet with."
  value       = google_service_account.cloud_run_runtime.email
}

output "github_deployer_service_account_email" {
  description = "Value for the GCP_SERVICE_ACCOUNT GitHub Actions secret."
  value       = google_service_account.github_deployer.email
}

output "github_workload_identity_provider" {
  description = "Value for the GCP_WORKLOAD_IDENTITY_PROVIDER GitHub Actions secret."
  value       = google_iam_workload_identity_pool_provider.github_actions.name
}
