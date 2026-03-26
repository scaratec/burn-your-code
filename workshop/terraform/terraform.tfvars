# Static defaults shared across all workshop deployments.
#
# project_id and processor_image are intentionally absent — both are
# project-specific and are always supplied by the Makefile via -var flags:
#
#   make tf-apply   PROJECT=<your-gcp-project-id>
#   make test-mi4   PROJECT=<your-gcp-project-id>
#
# This prevents accidental provisioning into the wrong GCP project.

region              = "europe-west3"
service_name        = "geofence-processor"
pubsub_topic        = "equiguard-telemetry"
pubsub_subscription = "equiguard-telemetry-push-sub"
