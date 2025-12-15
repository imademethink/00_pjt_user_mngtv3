import logging
from fastapi import APIRouter, HTTPException
import uuid, random
from user_mngt_app.database import get_connection
from user_mngt_app.validators import validate_email, validate_password, validate_otp

logger = logging.getLogger("user_mngt.v3")
router = APIRouter()

@router.post("/register/init")
def register_init(payload: dict):
    logger.debug("v3 register_init request payload=%s", payload)
    email = payload.get("email")
    if not validate_email(email):
        logger.debug("Invalid email: %s", email)
        raise HTTPException(status_code=400, detail="Invalid email")

    otp = str(random.randint(100000, 999999))
    session_key = str(uuid.uuid4())
    logger.debug("Generated otp=%s session_key=%s", otp, session_key)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT is_active FROM user_mngt_users WHERE email=?", (email,))
    row = cur.fetchone()

    if row and row[0] == 1:
        logger.debug("Duplicate active email: %s", email)
        conn.close()
        raise HTTPException(status_code=403, detail="Duplicate email")

    if row:
        cur.execute("UPDATE user_mngt_users SET otp=?, session_key=? WHERE email=?", (otp, session_key, email))
        logger.debug("Updated OTP/session for existing inactive user")
    else:
        cur.execute(
            "INSERT INTO user_mngt_users (email, password, otp, session_key, is_active) VALUES (?,?,?,?,0)",
            (email, "", otp, session_key)
        )
        logger.debug("Inserted new inactive user with OTP")

    conn.commit()
    conn.close()
    return {"otp": otp, "session_key": session_key}

@router.post("/register/complete")
def register_complete(payload: dict):
    logger.debug("v3 register_complete payload=%s", payload)
    email = payload.get("email")
    password = payload.get("password")
    otp = payload.get("otp")
    session_key = payload.get("session_key")

    if not all([validate_email(email), validate_password(password), validate_otp(otp)]):
        logger.debug("Validation failed for register_complete")
        raise HTTPException(status_code=400, detail="Validation failed")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE user_mngt_users SET password=?, is_active=1, otp=NULL "
        "WHERE email=? AND otp=? AND session_key=? AND is_active=0",
        (password, email, otp, session_key)
    )
    conn.commit()

    if cur.rowcount == 0:
        logger.debug("Invalid or expired OTP for email=%s", email)
        conn.close()
        raise HTTPException(status_code=403, detail="Invalid or expired OTP")

    conn.close()
    logger.debug("Registration completed for email=%s", email)
    return {"message": "Registration completed successfully"}