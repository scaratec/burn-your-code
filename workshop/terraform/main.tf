terraform {
  required_version = ">= 1.7"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ---------------------------------------------------------------------------
# Required APIs
# ---------------------------------------------------------------------------

resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "pubsub.googleapis.com",
    "firestore.googleapis.com",
    "artifactregistry.googleapis.com",
  ])
  service            = each.value
  disable_on_destroy = false
}

# ---------------------------------------------------------------------------
# Artifact Registry
# ---------------------------------------------------------------------------

resource "google_artifact_registry_repository" "equiguard" {
  repository_id = "equiguard"
  format        = "DOCKER"
  location      = var.region
  description   = "EquiGuard container images"

  depends_on = [google_project_service.apis]
}

# ---------------------------------------------------------------------------
# Cloud Run — Geofence Processor
# ---------------------------------------------------------------------------

resource "google_cloud_run_v2_service" "processor" {
  name     = var.service_name
  location = var.region

  template {
    containers {
      image = var.processor_image

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      ports {
        container_port = 8081
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "256Mi"
        }
      }
    }
  }

  depends_on = [google_project_service.apis]
}

# Allow the Pub/Sub service account to invoke the Cloud Run service
data "google_project" "project" {
  project_id = var.project_id
}

resource "google_cloud_run_v2_service_iam_member" "pubsub_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.processor.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}

# ---------------------------------------------------------------------------
# Pub/Sub — Topic & push subscription
# ---------------------------------------------------------------------------

resource "google_pubsub_topic" "telemetry" {
  name = var.pubsub_topic

  depends_on = [google_project_service.apis]
}

resource "google_pubsub_subscription" "telemetry_push" {
  name  = var.pubsub_subscription
  topic = google_pubsub_topic.telemetry.name

  push_config {
    push_endpoint = "${google_cloud_run_v2_service.processor.uri}/telemetry-push"
  }

  ack_deadline_seconds = 60

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "60s"
  }

  depends_on = [google_cloud_run_v2_service_iam_member.pubsub_invoker]
}
