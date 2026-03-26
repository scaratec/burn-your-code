# Static defaults shared across all workshop deployments.
#
# project_id and processor_image are intentionally absent — both are
# derived automatically by the Makefile from the project_id row in
# bdd/mi4_cloud_run.feature (the single source of truth) and passed
# to Terraform via -var flags. No manual edit of this file is needed.

region              = "europe-west3"
service_name        = "geofence-processor"
pubsub_topic        = "equiguard-telemetry"
pubsub_subscription = "equiguard-telemetry-push-sub"
