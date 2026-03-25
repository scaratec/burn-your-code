output "cloud_run_url" {
  description = "Public URL of the geofence-processor Cloud Run service"
  value       = google_cloud_run_v2_service.processor.uri
}

output "registry_hostname" {
  description = "Artifact Registry hostname for docker push/pull"
  value       = "${var.region}-docker.pkg.dev"
}

output "registry_image_base" {
  description = "Base path for images in Artifact Registry"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/equiguard"
}

output "topic_path" {
  description = "Full Pub/Sub topic resource path for the publisher client"
  value       = "projects/${var.project_id}/topics/${var.pubsub_topic}"
}

output "project_id" {
  value = var.project_id
}

output "region" {
  value = var.region
}
