project_id          = "randy-gupta-poc"
region              = "europe-west3"
service_name        = "geofence-processor"
pubsub_topic        = "equiguard-telemetry"
pubsub_subscription = "equiguard-telemetry-push-sub"

# Set this after running 'make push-image':
# europe-west3-docker.pkg.dev/randy-gupta-poc/equiguard/geofence-processor:v1
processor_image = "europe-west3-docker.pkg.dev/randy-gupta-poc/equiguard/geofence-processor:v1"
