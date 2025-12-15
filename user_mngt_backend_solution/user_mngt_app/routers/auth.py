import logging
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from user_mngt_app.database import get_connection
from user_mngt_app.validators import validate_email, validate_password
from user_mngt_app.config import (
    USER_MNGT_MAX_LOGIN_ATTEMPTS,
    USER_MNGT_ACCOUNT_LOCK_MINUTES
)

logger = logging.getLogger("user_mngt.auth")
router = APIRouter()

@router.post("/login")
def login(payload: dict):
    email = payload.get("email")
    password = payload.get("password")

    logger.debug("Login attempt email=%s", email)

    if not validate_email(email) or not validate_password(password):
        raise HTTPException(status_code=400, detail="Validation failed")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT password, failed_login_attempts, lock_until, is_active "
        "FROM user_mngt_users WHERE email=?",
        (email,)
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db_password, failed_attempts, lock_until, is_active = row

    if lock_until:
        lock_until_dt = datetime.fromisoformat(lock_until)
        if datetime.utcnow() < lock_until_dt:
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="account is locked please try after sometime"
            )

    if password != db_password or not is_active:
        failed_attempts = (failed_attempts or 0) + 1
        lock_until_val = None

        if failed_attempts >= USER_MNGT_MAX_LOGIN_ATTEMPTS:
            lock_until_val = (
                datetime.utcnow() +
                timedelta(minutes=USER_MNGT_ACCOUNT_LOCK_MINUTES)
            ).isoformat()

        cur.execute(
            "UPDATE user_mngt_users SET failed_login_attempts=?, lock_until=? "
            "WHERE email=?",
            (failed_attempts, lock_until_val, email)
        )
        conn.commit()
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_key = str(uuid.uuid4())
    cur.execute(
        "UPDATE user_mngt_users SET session_key=?, failed_login_attempts=0, lock_until=NULL "
        "WHERE email=?",
        (session_key, email)
    )
    conn.commit()
    conn.close()

    logger.debug("Login successful email=%s", email)
    return {"session_key": session_key}


@router.post("/logout")
def logout(payload: dict):
    logger.debug("Logout request payload=%s", payload)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE user_mngt_users SET session_key=NULL WHERE email=? AND session_key=?",
        (payload.get("email"), payload.get("session_key"))
    )
    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid session")

    conn.close()
    return {"message": "Logout successful"}


@router.post("/forget_password")
def forget_password(payload: dict):
    logger.debug("Forget password payload=%s", payload)

    email = payload.get("email")
    new_password = payload.get("new_password")
    confirm_password = payload.get("confirm_new_password")
    session_key = payload.get("session_key")

    if not validate_email(email) or not validate_password(new_password):
        raise HTTPException(status_code=400, detail="Validation failed")

    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE user_mngt_users SET password=? "
        "WHERE email=? AND session_key=? AND is_active=1",
        (new_password, email, session_key)
    )
    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=403, detail="Invalid session or email")

    conn.close()
    return {"message": "Password updated successfully"}


@router.post("/refresh_session")
def refresh_session(payload: dict):
    email = payload.get("email")
    current_session_key = payload.get("session_key")
    password = payload.get("password")

    logger.debug("Refresh session request email=%s", email)

    if not validate_email(email) or not validate_password(password):
        raise HTTPException(status_code=400, detail="Validation failed")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM user_mngt_users "
        "WHERE email=? AND password=? AND session_key=? AND is_active=1",
        (email, password, current_session_key)
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials or session")

    new_session_key = str(uuid.uuid4())

    cur.execute(
        "UPDATE user_mngt_users SET session_key=? WHERE email=?",
        (new_session_key, email)
    )
    conn.commit()
    conn.close()

    logger.debug("Session refreshed email=%s", email)
    return {"session_key": new_session_key}