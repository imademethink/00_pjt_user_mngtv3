
TEST_DATA = {
    "email": "demo111@test.com",
    "password": "ab12CD",
    "otp": "123456"
}

ENDPOINTS = {
    "register_init": "/api/v3/users/register/init",
    "register_complete": "/api/v3/users/register/complete",
    "login": "/api/v1/users/login",
    "logout": "/api/v1/users/logout",
    "profile": "/api/v1/prefix_user",
    "forget_password": "/api/v1/users/forget_password",
    "version": "/api/v1/version"
}

EXPECTED_STATUS = {
    "register_init": [200, 400, 403],
    "register_complete": [201, 400, 403],
    "login": [200, 401],
    "logout": [200, 401],
    "profile_get": [200, 403],
    "profile_update": [200, 400, 403],  # FIXED HERE
    "delete": [202, 401],
    "forget_password": [200, 400, 403],
    "version": [200]
}

RESPONSE_SCHEMAS = {
    "register_init": {
        "type": "object",
        "required": ["otp", "session_key"],
        "properties": {
            "otp": {"type": "string"},
            "session_key": {"type": "string"}
        }
    },
    "login": {
        "type": "object",
        "required": ["session_key"],
        "properties": {
            "session_key": {"type": "string"}
        }
    },
    "version": {
        "type": "object",
        "required": ["version"],
        "properties": {
            "version": {"type": "string"}
        }
    }
}

PROFILE_PAYLOAD = {
    "first_name": "Jonathan",
    "last_name": "Williams",
    "country": "Indiaaa",
    "pin_code": "560001",
    "contact_country_code": "091",
    "contact_number": "9876543210"
}
