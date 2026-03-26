import json
import os
import subprocess
import time

import requests
from behave import given, then, when
from google.cloud import firestore, pubsub_v1


def _id_token() -> str:
    """Fetch a Google OIDC identity token for the authenticated gcloud user.

    Uses 'gcloud auth print-identity-token' which works with all gcloud
    credential types including application-default user credentials.
    Cloud Run accepts tokens issued by accounts with roles/run.invoker.
    """
    result = subprocess.run(
        ["gcloud", "auth", "print-identity-token"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

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

    # project_id is the single source of truth — read directly from the
    # Gherkin Background table. The Makefile extracts the same value via
    # awk so that Terraform and Docker always use an identical project ID
    # without any additional configuration files or CLI flags.
    context.project_id = context.cloud_config["project_id"]

    # Ensure real Firestore is used — not the local emulator
    os.environ.pop("FIRESTORE_EMULATOR_HOST", None)
    context.db = firestore.Client(project=context.project_id)


@given("the infrastructure is provisioned with Terraform")
def step_terraform_read_outputs(context):
    """Assert that Terraform-managed infrastructure is deployed and read its
    outputs into the test context.

    This step deliberately does NOT run 'terraform apply'. Provisioning is a
    deployment concern, not a test concern. The step fails with a clear message
    when the infrastructure has not been provisioned yet, guiding the user to
    run 'make tf-apply' first.

    Outputs are cached on context.feature so that only the first scenario in
    the feature run pays the cost of a 'terraform output' call. All subsequent
    scenarios reuse the cached values.
    """
    # Cache outputs across scenarios within the same feature run.
    if getattr(context.feature, "_tf_outputs_loaded", False):
        context.cloud_run_url = context.feature._tf_cloud_run_url
        context.topic_path    = context.feature._tf_topic_path
        context.publisher     = context.feature._tf_publisher
        return

    result = subprocess.run(
        ["terraform", "output", "-json"],
        cwd=_TERRAFORM_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Could not read Terraform outputs — has the infrastructure been "
            "provisioned?\n\nRun 'make tf-apply' and try again.\n\n"
            f"terraform output stderr:\n{result.stderr}"
        )

    outputs = json.loads(result.stdout)
    if not outputs:
        raise RuntimeError(
            "Terraform outputs are empty — the infrastructure may not have "
            "been provisioned yet.\n\nRun 'make tf-apply' and try again."
        )

    context.cloud_run_url = outputs["cloud_run_url"]["value"]
    context.topic_path    = outputs["topic_path"]["value"]
    context.publisher     = pubsub_v1.PublisherClient()

    # Cache on feature so subsequent scenarios skip the subprocess call.
    context.feature._tf_outputs_loaded  = True
    context.feature._tf_cloud_run_url   = context.cloud_run_url
    context.feature._tf_topic_path      = context.topic_path
    context.feature._tf_publisher       = context.publisher


# ---------------------------------------------------------------------------
# Action steps
# ---------------------------------------------------------------------------

@when(
    'a Pub/Sub message is published to topic "{topic}"'
    ' for "{device_id}":'
)
def step_publish_pubsub(context, topic, device_id):
    payload = json.loads(context.text)

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
            token = _id_token()
            resp = requests.get(
                url,
                timeout=5,
                headers={"Authorization": f"Bearer {token}"},
            )
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
