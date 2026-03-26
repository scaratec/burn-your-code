"""Behave environment hooks for the EquiGuard BDD test suite.

after_scenario runs after every scenario across all milestones and is
responsible for two cleanup concerns:

1. Process / container teardown (MI2, MI3)
   Stop the geofence-processor binary (MI2) or Docker container (MI3) that
   was started by the Given step so that the next scenario gets a clean slate
   and no port conflicts arise.

2. Firestore data teardown (MI1–MI4)
   Delete all documents written during the scenario so that assertion steps
   in later scenarios do not see stale data from earlier runs.

   MI1–MI3 (emulator): the Firestore emulator exposes an HTTP DELETE endpoint
   that wipes an entire project in one call — fast and atomic.

   MI4 (real Firestore): documents are streamed and deleted individually.
   Only the 'alerts' and 'geofences' collections are touched; no other
   production data is at risk.
"""

import os
import subprocess

import requests
from google.cloud import firestore


def before_feature(context, feature):
    """Guard against leftover Firestore data from aborted previous runs.

    after_scenario cleans up after every scenario, but if a run is killed
    (Ctrl+C, CI timeout, OOM) the After hooks do not execute and stale
    documents remain in real Firestore. This hook runs once before the first
    scenario of the MI4 feature and ensures a clean slate regardless of how
    the previous run ended.

    Only active for MI4 (tagged @mi4) and only against real Firestore —
    emulator state is ephemeral and does not persist across runs.
    """
    if "mi4" not in feature.tags:
        return
    if os.environ.get("FIRESTORE_EMULATOR_HOST"):
        return

    project_id = context.config.userdata.get("project_id")
    if not project_id:
        return  # project unknown at this point — step code will fail later

    try:
        db = firestore.Client(project=project_id)
        for collection in ("alerts", "geofences"):
            for doc in db.collection(collection).stream():
                doc.reference.delete()
    except Exception as exc:
        print(f"WARNING: before_feature cleanup failed: {exc}")


def after_scenario(context, scenario):
    # -------------------------------------------------------------------------
    # 1. Stop containerized or in-process service (MI2, MI3)
    # -------------------------------------------------------------------------
    if hasattr(context, "container_id"):
        subprocess.run(
            ["docker", "stop", context.container_id], capture_output=True
        )
        subprocess.run(
            ["docker", "rm", context.container_id], capture_output=True
        )

    if hasattr(context, "processor_process"):
        context.processor_process.terminate()
        context.processor_process.wait()

    # -------------------------------------------------------------------------
    # 2. Clear Firestore data written during the scenario
    # -------------------------------------------------------------------------
    if not hasattr(context, "project_id"):
        return  # MI1 — no Firestore involved

    emulator_host = os.environ.get("FIRESTORE_EMULATOR_HOST")

    if emulator_host:
        # MI2 / MI3 — wipe the whole emulator project in one HTTP call.
        url = (
            f"http://{emulator_host}/emulator/v1/projects"
            f"/{context.project_id}/databases/(default)/documents"
        )
        try:
            requests.delete(url)
        except Exception as exc:
            print(f"WARNING: Failed to clear Firestore emulator: {exc}")
    else:
        # MI4 — delete individual documents from real Firestore.
        # Only 'alerts' and 'geofences' are written by the test suite.
        try:
            for collection in ("alerts", "geofences"):
                for doc in context.db.collection(collection).stream():
                    doc.reference.delete()
        except Exception as exc:
            print(f"WARNING: Failed to clear real Firestore: {exc}")
