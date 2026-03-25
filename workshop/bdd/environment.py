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
        emulator_host = os.environ.get("FIRESTORE_EMULATOR_HOST", "localhost:8082")
        url = f"http://{emulator_host}/emulator/v1/projects/{context.project_id}/databases/(default)/documents"
        try:
            requests.delete(url)
        except Exception as e:
            print(f"Failed to clear firestore emulator: {e}")
