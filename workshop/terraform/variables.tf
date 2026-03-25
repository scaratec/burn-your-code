variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "randy-gupta-poc"
}

variable "region" {
  description = "GCP region for all resources"
  type        = string
  default     = "europe-west3"
}

variable "service_name" {
  description = "Cloud Run service name"
  type        = string
  default     = "geofence-processor"
}

variable "pubsub_topic" {
  description = "Pub/Sub topic name for telemetry events"
  type        = string
  default     = "equiguard-telemetry"
}

variable "pubsub_subscription" {
  description = "Pub/Sub push subscription name"
  type        = string
  default     = "equiguard-telemetry-push-sub"
}

variable "processor_image" {
  description = "Full Artifact Registry image URL for the geofence-processor"
  type        = string
  # Set via terraform.tfvars or TF_VAR_processor_image after docker push
}
