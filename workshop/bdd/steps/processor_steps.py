import json
import subprocess
import time
import requests
import os
import base64
from behave import given, when, then
from google.cloud import firestore

@given('the geofence-processor is configured with:')
def step_given_processor_config(context):
    config = {}
    for row in context.table:
        config[row["key"]] = row["value"]
    
    # Set environment variables for the Go app
    env = os.environ.copy()
    env["FIRESTORE_EMULATOR_HOST"] = config["firestore-emulator-host"]
    env["PUBSUB_EMULATOR_HOST"] = config.get("pubsub-emulator-host", "")
    env["PROJECT_ID"] = config["firestore-project-id"]
    env["PORT"] = config["port"]
    
    # We also need to set FIRESTORE_EMULATOR_HOST in our python environment
    # so that the google-cloud-firestore client uses it.
    os.environ["FIRESTORE_EMULATOR_HOST"] = config["firestore-emulator-host"]
    
    context.processor_port = config["port"]
    context.project_id = config["firestore-project-id"]
    
    # Create firestore client for the test
    context.db = firestore.Client(project=context.project_id)
    
    # Compile the Go app if not already compiled
    if not hasattr(context, 'go_compiled'):
        subprocess.run(["go", "build", "-o", "bin/geofence-processor", "cmd/geofence-processor/main.go"], check=True)
        context.go_compiled = True
        
    # Start the Go app
    context.processor_process = subprocess.Popen(["./bin/geofence-processor"], env=env)
    
    # Wait for the server to be ready
    time.sleep(1)


@given('the Firestore collection "{collection}" contains the document "{document_id}":')
def step_given_firestore_doc(context, collection, document_id):
    data = json.loads(context.text)
    context.db.collection(collection).document(document_id).set(data)


@when('the service receives a Pub/Sub push event on "{endpoint}" for "{device_id}":')
def step_when_pubsub_push(context, endpoint, device_id):
    payload = json.loads(context.text)
    # Inject device_id so the processor knows which horse it is
    payload["device"] = device_id
    
    # Wrap in Pub/Sub push format
    data_bytes = json.dumps(payload).encode("utf-8")
    b64_data = base64.b64encode(data_bytes).decode("utf-8")
    
    push_message = {
        "message": {
            "data": b64_data,
            "messageId": "12345"
        }
    }
    
    url = f"http://localhost:{context.processor_port}{endpoint}"
    resp = requests.post(url, json=push_message)
    resp.raise_for_status()


@then('the Firestore collection "{collection}" should eventually contain a record for "{device_id}":')
def step_then_eventually_contains(context, collection, device_id):
    expected_data = {}
    for row in context.table:
        expected_data[row["field"]] = row["value"]
        
    max_retries = 20
    delay_seconds = 0.5
    success = False
    
    for i in range(max_retries):
        try:
            # Check Firestore
            docs = context.db.collection(collection).where("device", "==", device_id).stream()
            for doc in docs:
                doc_dict = doc.to_dict()
                # Check if all expected fields match
                matches = True
                for k, v in expected_data.items():
                    if doc_dict.get(k) != v:
                        matches = False
                        break
                if matches:
                    success = True
                    break
        except Exception as e:
            pass
            
        if success:
            break
            
        print(f"Waiting for async Firestore write (Attempt {i+1}/{max_retries})...")
        time.sleep(delay_seconds)
        
    if not success:
        raise AssertionError(f"Alert not written to Firestore within timeout for device {device_id}")


@then('the Firestore collection "{collection}" should not contain a record for "{device_id}" within {seconds:d} seconds')
def step_then_should_not_contain(context, collection, device_id, seconds):
    # Wait the given seconds
    time.sleep(seconds)
    
    docs = list(context.db.collection(collection).where("device", "==", device_id).stream())
    if len(docs) > 0:
        raise AssertionError(f"Found unexpected record for device {device_id}")
