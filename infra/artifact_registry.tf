resource "google_artifact_registry_repository" "api_images" {
  project       = var.project_id
  location      = var.region
  repository_id = "garden-tasks-api-repo"
  description   = "Docker repository for Garden Tasks API"
  format        = "DOCKER"

  depends_on = [
    google_project_service.project_services["artifactregistry.googleapis.com"],
  ]
}
