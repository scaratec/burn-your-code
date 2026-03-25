import base64
import json
import os
import subprocess
import time

import requests
from behave import given, then, when
from google.cloud import firestore


@given('the geofence-processor image is built from "{context_path}" with tag "{tag}"')
def step_build_image(context, context_path, tag):
    result = subprocess.run(
        ["docker", "build", "-t", tag, context_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"docker build failed:\n{result.stderr}")
    context.image_tag = tag


@given("the container is started with the following configuration:")
def step_start_container(context):
    config = {row["key"]: row["value"] for row in context.table}

    host_port = config["host_port"]
    container_port = config["container_port"]
    network = config.get("network", "bridge")

    env_vars = {
        k: v
        for k, v in config.items()
        if k not in ("host_port", "container_port", "network")
    }

    cmd = [
        "docker", "run", "-d",
        f"--network={network}",
        "-p", f"{host_port}:{container_port}",
    ]
    for k, v in env_vars.items():
        cmd += ["-e", f"{k}={v}"]
    cmd.append(context.image_tag)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"docker run failed:\n{result.stderr}")

    context.container_id = result.stdout.strip()
    context.container_port = host_port
    context.project_id = env_vars.get("PROJECT_ID", "equiguard-test")

    os.environ["FIRESTORE_EMULATOR_HOST"] = env_vars.get(
        "FIRESTORE_EMULATOR_HOST", "localhost:8082"
    )
    context.db = firestore.Client(project=context.project_id)


@then(
    'the container health endpoint "{method_path}" should respond'
    " with status {expected_status:d} within {timeout:d} seconds"
)
def step_health_check(context, method_path, expected_status, timeout):
    # Parse "GET /health" — method is informational, we always GET
    path = method_path.split(" ", 1)[-1]
    url = f"http://localhost:{context.container_port}{path}"
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            resp = requests.get(url, timeout=1)
            if resp.status_code == expected_status:
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)

    raise AssertionError(
        f"Health endpoint {url} did not respond with HTTP {expected_status}"
        f" within {timeout}s"
    )


@then("the container should listen on port {expected_port:d}")
def step_check_port(context, expected_port):
    result = subprocess.run(
        [
            "docker", "inspect",
            "--format",
            "{{range $k, $v := .NetworkSettings.Ports}}{{$k}} {{end}}",
            context.container_id,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"docker inspect failed:\n{result.stderr}")

    assert f"{expected_port}/tcp" in result.stdout, (
        f"Expected port {expected_port}/tcp not exposed."
        f" Found: {result.stdout.strip()}"
    )


@when(
    'the containerized service receives a Pub/Sub push event'
    ' on "{endpoint}" for "{device_id}":'
)
def step_container_pubsub_push(context, endpoint, device_id):
    payload = json.loads(context.text)
    payload["device"] = device_id

    b64_data = base64.b64encode(
        json.dumps(payload).encode("utf-8")
    ).decode("utf-8")

    push_message = {
        "message": {"data": b64_data, "messageId": "12345"}
    }

    url = f"http://localhost:{context.container_port}{endpoint}"
    requests.post(url, json=push_message).raise_for_status()


@when(
    'the containerized service receives a malformed push event'
    ' on "{endpoint}":'
)
def step_container_malformed_push(context, endpoint):
    payload = json.loads(context.text)

    b64_data = base64.b64encode(
        json.dumps(payload).encode("utf-8")
    ).decode("utf-8")

    push_message = {
        "message": {"data": b64_data, "messageId": "99999"}
    }

    url = f"http://localhost:{context.container_port}{endpoint}"
    # Store response for the subsequent Then step — do not raise on 4xx
    context.last_response = requests.post(url, json=push_message)


@then("the response status should be {expected_status:d}")
def step_response_status(context, expected_status):
    actual = context.last_response.status_code
    assert actual == expected_status, (
        f"Expected HTTP {expected_status}, got {actual}"
    )


@then('the Firestore collection "{collection}" should remain empty')
def step_firestore_remains_empty(context, collection):
    # Negative assertion: we must wait briefly to catch any unintended
    # async write. 1 s matches the processor's observed write latency.
    time.sleep(1)
    docs = list(context.db.collection(collection).stream())
    assert len(docs) == 0, (
        f"Expected '{collection}' to be empty, found {len(docs)} document(s)"
    )
