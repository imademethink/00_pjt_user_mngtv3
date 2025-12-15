
from config.test_metadata import (
    TEST_DATA, ENDPOINTS, EXPECTED_STATUS, RESPONSE_SCHEMAS, PROFILE_PAYLOAD
)
from utils.response_validator import validate_response

def test_register_init(api_client, context):
    r = api_client.call("POST", ENDPOINTS["register_init"], json={"email": TEST_DATA["email"]})
    validate_response(r, EXPECTED_STATUS["register_init"], RESPONSE_SCHEMAS["register_init"])
    if r.status_code == 200:
        context["session_key"] = r.json()["session_key"]

def test_register_complete(api_client, context):
    r = api_client.call(
        "POST", ENDPOINTS["register_complete"],
        json={
            "email": TEST_DATA["email"],
            "password": TEST_DATA["password"],
            "otp": TEST_DATA["otp"],
            "session_key": context.get("session_key", "")
        }
    )
    validate_response(r, EXPECTED_STATUS["register_complete"])

def test_login(api_client, context):
    r = api_client.call("POST", ENDPOINTS["login"], json={"email": TEST_DATA["email"], "password": TEST_DATA["password"]})
    validate_response(r, EXPECTED_STATUS["login"], RESPONSE_SCHEMAS["login"])
    if r.status_code == 200:
        context["session_key"] = r.json()["session_key"]

def test_get_profile(api_client, context):
    r = api_client.call("GET", ENDPOINTS["profile"], params={"email": TEST_DATA["email"], "session_key": context.get("session_key","")})
    validate_response(r, EXPECTED_STATUS["profile_get"])

def test_update_profile(api_client, context):
    payload = {"email": TEST_DATA["email"], "session_key": context.get("session_key","")}
    payload.update(PROFILE_PAYLOAD)
    r = api_client.call("PUT", ENDPOINTS["profile"], json=payload)
    validate_response(r, EXPECTED_STATUS["profile_update"])

def test_logout(api_client, context):
    r = api_client.call("POST", ENDPOINTS["logout"], json={"email": TEST_DATA["email"], "session_key": context.get("session_key","")})
    validate_response(r, EXPECTED_STATUS["logout"])

def test_delete_user(api_client, context):
    r = api_client.call(
        "DELETE", ENDPOINTS["profile"],
        json={"email": TEST_DATA["email"], "password": TEST_DATA["password"], "session_key": context.get("session_key","")}
    )
    validate_response(r, EXPECTED_STATUS["delete"])

def test_forget_password(api_client, context):
    r = api_client.call(
        "POST", ENDPOINTS["forget_password"],
        json={
            "email": TEST_DATA["email"],
            "new_password": TEST_DATA["password"],
            "confirm_new_password": TEST_DATA["password"],
            "session_key": context.get("session_key","")
        }
    )
    validate_response(r, EXPECTED_STATUS["forget_password"])

def test_version(api_client):
    r = api_client.call("GET", ENDPOINTS["version"])
    validate_response(r, EXPECTED_STATUS["version"], RESPONSE_SCHEMAS["version"])
