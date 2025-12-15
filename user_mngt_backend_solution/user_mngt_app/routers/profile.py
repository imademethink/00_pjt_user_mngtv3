import logging
from fastapi import APIRouter, HTTPException
from user_mngt_app.database import get_connection
from user_mngt_app.validators import (
    validate_name,
    validate_generic,
    validate_country_code,
    validate_contact,
    validate_password
)

logger = logging.getLogger("user_mngt.profile")
router = APIRouter()

@router.get("/prefix_user")
def get_user(email: str, session_key: str):
    logger.debug("Get user email=%s session_key=%s", email, session_key)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT email, first_name, last_name, country "
        "FROM user_mngt_users "
        "WHERE email=? AND session_key=? AND session_key IS NOT NULL",
        (email, session_key)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        logger.debug("Invalid or logged-out session in get_user")
        raise HTTPException(status_code=403, detail="Invalid session")
    return dict(zip(["email", "first_name", "last_name", "country"], row))


@router.put("/prefix_user")
def update_user(payload: dict):
    logger.debug("Update user payload=%s", payload)

    if not all([
        validate_name(payload.get("first_name")),
        validate_name(payload.get("last_name")),
        validate_generic(payload.get("country")),
        validate_generic(payload.get("pin_code")),
        validate_country_code(payload.get("contact_country_code")),
        validate_contact(payload.get("contact_number")),
        validate_password(payload.get("password"))
    ]):
        logger.debug("Validation failed in update_user")
        raise HTTPException(status_code=400, detail="Validation failed")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE user_mngt_users SET "
        "first_name=?, last_name=?, country=?, pin_code=?, "
        "contact_country_code=?, contact_number=?, password=? "
        "WHERE email=? AND session_key=? AND session_key IS NOT NULL",
        (
            payload["first_name"],
            payload["last_name"],
            payload["country"],
            payload["pin_code"],
            payload["contact_country_code"],
            payload["contact_number"],
            payload["password"],
            payload["email"],
            payload["session_key"]
        )
    )
    conn.commit()

    if cur.rowcount == 0:
        logger.debug("Invalid or logged-out session in update_user")
        conn.close()
        raise HTTPException(status_code=403, detail="Invalid session")

    conn.close()
    logger.debug("User updated successfully email=%s", payload["email"])
    return {"message": "User updated successfully"}


@router.delete("/prefix_user")
def delete_user(payload: dict):
    logger.debug("Delete user payload=%s", payload)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM user_mngt_users "
        "WHERE email=? AND password=? AND session_key=? AND session_key IS NOT NULL",
        (payload.get("email"), payload.get("password"), payload.get("session_key"))
    )
    conn.commit()

    if cur.rowcount == 0:
        logger.debug("Invalid credentials or logged-out session in delete_user")
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials or session")

    conn.close()
    logger.debug("User deleted successfully email=%s", payload.get("email"))
    return {"message": "User deleted successfully"}