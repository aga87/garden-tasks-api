output "github_deployer_service_account_email" {
  description = "Value for the GCP_SERVICE_ACCOUNT GitHub Actions secret."
  value       = google_service_account.github_deployer.email
}

output "github_workload_identity_provider" {
  description = "Value for the GCP_WORKLOAD_IDENTITY_PROVIDER GitHub Actions secret."
  value       = google_iam_workload_identity_pool_provider.github_actions.name
}
