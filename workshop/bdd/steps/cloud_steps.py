import json
import os
import subprocess
import time

import requests
from behave import given, then, when
from google.cloud import firestore, pubsub_v1

# Absolute path to the Terraform directory relative to this file
_TERRAFORM_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "terraform"
)


# ---------------------------------------------------------------------------
# Background steps
# ---------------------------------------------------------------------------

@given("the Cloud Run deployment is configured with:")
def step_cloud_config(context):
    context.cloud_config = {row["key"]: row["value"] for row in context.table}
    context.project_id = context.cloud_config["project_id"]

    # Ensure real Firestore is used — not the local emulator
    os.environ.pop("FIRESTORE_EMULATOR_HOST", None)
    context.db = firestore.Client(project=context.project_id)


@given("the infrastructure is provisioned with Terraform")
def step_terraform_apply(context):
    # terraform init — safe to run repeatedly
    subprocess.run(
        ["terraform", "init", "-input=false"],
        cwd=_TERRAFORM_DIR,
        check=True,
    )

    # terraform apply — idempotent, only changes drift
    result = subprocess.run(
        ["terraform", "apply", "-auto-approve", "-input=false"],
        cwd=_TERRAFORM_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"terraform apply failed:\n{result.stderr}")

    # Read outputs so subsequent steps can use them
    output_result = subprocess.run(
        ["terraform", "output", "-json"],
        cwd=_TERRAFORM_DIR,
        capture_output=True,
        text=True,
        check=True,
    )
    outputs = json.loads(output_result.stdout)

    context.cloud_run_url = outputs["cloud_run_url"]["value"]
    context.topic_path = outputs["topic_path"]["value"]
    context.publisher = pubsub_v1.PublisherClient()


# ---------------------------------------------------------------------------
# Action steps
# ---------------------------------------------------------------------------

@when(
    'a Pub/Sub message is published to topic "{topic}"'
    ' for "{device_id}":'
)
def step_publish_pubsub(context, topic, device_id):
    payload = json.loads(context.text)
    payload["device"] = device_id

    data = json.dumps(payload).encode("utf-8")
    # Block until the message is confirmed by the Pub/Sub service
    future = context.publisher.publish(context.topic_path, data)
    future.result()


# ---------------------------------------------------------------------------
# Assertion steps
# ---------------------------------------------------------------------------

@then(
    'the Cloud Run service health endpoint "{method_path}" should respond'
    " with status {expected_status:d} within {timeout:d} seconds"
)
def step_cloud_health_check(context, method_path, expected_status, timeout):
    path = method_path.split(" ", 1)[-1]
    url = f"{context.cloud_run_url}{path}"
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == expected_status:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(2)

    raise AssertionError(
        f"Health endpoint {url} did not respond with"
        f" HTTP {expected_status} within {timeout}s"
    )


# The following Then-steps are reused from processor_steps.py — Behave
# loads all step files globally so no re-implementation is needed:
#
#   "the Firestore collection ... should eventually contain a record for ..."
#   "the Firestore collection ... should not contain a record for ... within N s"
#
# Both work with context.db, which is set to real Firestore in this module.
