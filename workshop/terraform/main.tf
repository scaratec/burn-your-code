terraform {
  required_version = ">= 1.7"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # ---------------------------------------------------------------------------
  # Remote backend (recommended for teams)
  #
  # By default Terraform stores state locally in terraform.tfstate, which is
  # excluded from version control via .gitignore. This is fine when a single
  # person runs 'make tf-apply', but breaks in team settings because two
  # people would maintain separate, diverging state files.
  #
  # To use a shared GCS backend:
  #   1. Create a GCS bucket:
  #        gsutil mb -l europe-west3 gs://<your-project-id>-tf-state
  #        gsutil versioning set on gs://<your-project-id>-tf-state
  #   2. Uncomment and fill in the block below.
  #   3. Run 'terraform init -migrate-state' to upload the existing state.
  #
  # backend "gcs" {
  #   bucket = "<your-project-id>-tf-state"
  #   prefix = "equiguard"
  # }
  # ---------------------------------------------------------------------------
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
# Firestore database
# ---------------------------------------------------------------------------

resource "google_firestore_database" "default" {
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
  depends_on  = [google_project_service.apis]
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
    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }

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
        # cpu_idle = true: CPU is throttled between requests (not always
        # allocated). Combined with Go's fast startup and small binary,
        # this is the cheapest viable Cloud Run configuration.
        cpu_idle = true
        limits = {
          cpu    = "1"
          memory = "256Mi"
        }
      }
    }
  }

  depends_on = [google_project_service.apis]
}

# Dedicated service account for Pub/Sub → Cloud Run push authentication.
# Using a dedicated SA (not the built-in gcp-sa-pubsub SA) avoids the
# iam.serviceAccounts.actAs permission requirement on the built-in SA,
# since the Terraform caller owns any SA it creates.
resource "google_service_account" "pusher" {
  account_id   = "equiguard-pusher"
  display_name = "EquiGuard Pub/Sub → Cloud Run Pusher"
  project      = var.project_id
}

resource "google_cloud_run_v2_service_iam_member" "pubsub_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.processor.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.pusher.email}"
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
    oidc_token {
      service_account_email = google_service_account.pusher.email
      audience              = google_cloud_run_v2_service.processor.uri
    }
  }

  ack_deadline_seconds = 60

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "60s"
  }

  depends_on = [google_cloud_run_v2_service_iam_member.pubsub_invoker]
}
