resource "google_project_service" "project_services" {
  for_each = toset([
    "artifactregistry.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "run.googleapis.com",
    "sheets.googleapis.com",
    "sts.googleapis.com",
  ])

  project = var.project_id
  service = each.value

  disable_on_destroy = false
}
