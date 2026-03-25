import os
import subprocess

import requests


def after_scenario(context, scenario):
    if hasattr(context, 'container_id'):
        subprocess.run(["docker", "stop", context.container_id],
                       capture_output=True)
        subprocess.run(["docker", "rm", context.container_id],
                       capture_output=True)

    if hasattr(context, 'processor_process'):
        context.processor_process.terminate()
        context.processor_process.wait()

    if hasattr(context, 'project_id'):
        emulator_host = os.environ.get("FIRESTORE_EMULATOR_HOST")

        if emulator_host:
            # MI1/MI2/MI3 — bulk-delete via emulator HTTP API
            url = (
                f"http://{emulator_host}/emulator/v1/projects"
                f"/{context.project_id}/databases/(default)/documents"
            )
            try:
                requests.delete(url)
            except Exception as e:
                print(f"Failed to clear Firestore emulator: {e}")
        else:
            # MI4 — delete documents individually against real Firestore
            try:
                for col in ("alerts", "geofences"):
                    for doc in context.db.collection(col).stream():
                        doc.reference.delete()
            except Exception as e:
                print(f"Failed to clear real Firestore: {e}")
