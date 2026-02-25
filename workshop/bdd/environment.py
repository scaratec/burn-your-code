import os
import requests

def after_scenario(context, scenario):
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
