import json
import subprocess
from behave import given, when, then

@given('the geofence "{geofence_id}" is defined by the following polygon:')
def step_given_geofence_polygon(context, geofence_id):
    if not hasattr(context, 'geofences'):
        context.geofences = {}
    
    polygon = []
    for row in context.table:
        polygon.append({
            "lon": float(row["longitude"]),
            "lat": float(row["latitude"])
        })
    
    context.geofences[geofence_id] = polygon


@when('I run the geofence library test "{command}" with:')
def step_when_run_library_test(context, command):
    params = {}
    for row in context.table:
        params[row["parameter"]] = row["value"]
    
    try:
        point_data = json.loads(params["point"])
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON in point parameter: {e}")
        
    polygon_id = params["polygon"]
    
    polygon = context.geofences.get(polygon_id)
    if not polygon:
        raise AssertionError(f"Geofence '{polygon_id}' not found in context.")
    
    if command == "is-point-inside":
        payload = {
            "point": point_data,
            "polygon": polygon
        }
        
        # Call the pre-built CLI wrapper (built by `make build`)
        cmd = ["./bin/geofence-lib-test"]

        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=json.dumps(payload))
        
        if process.returncode != 0:
            raise RuntimeError(f"Go wrapper failed: {stderr}")
            
        try:
            result = json.loads(stdout)
        except json.JSONDecodeError:
            raise RuntimeError(f"Failed to decode Go wrapper output: {stdout}")
            
        context.library_result = result.get("is_inside")
    else:
        raise NotImplementedError(f"Unknown library command: {command}")


@then('the library result should be "{expected_result}"')
def step_then_library_result(context, expected_result):
    expected_bool = expected_result.strip().lower() == "true"
    
    if not hasattr(context, 'library_result'):
        raise AssertionError("No library result in context. Did the previous step fail?")
        
    assert context.library_result == expected_bool, \
        f"Expected point to be {expected_bool}, but library returned {context.library_result}"