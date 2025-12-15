
from jsonschema import validate

def validate_response(response, expected_status, schema=None):
    if response.status_code not in expected_status:
        raise AssertionError(
            f"Expected {expected_status}, got {response.status_code}, body={response.text}"
        )

    if not schema:
        return

    if response.status_code not in (200, 201):
        return

    body = response.json()
    validate(instance=body, schema=schema)
