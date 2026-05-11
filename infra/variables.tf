variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "GCP region"
  default     = "europe-west3"
}

variable "github_repository" {
  type        = string
  description = "GitHub repository allowed to deploy via Workload Identity Federation, in owner/name format."
  default     = "aga87/garden-tasks-api"
}

variable "github_deploy_branch" {
  type        = string
  description = "Git branch allowed to deploy via Workload Identity Federation."
  default     = "main"
}
