
from fastapi import APIRouter, HTTPException
import uuid
from user_mngt_app.database import get_connection, init_db
from user_mngt_app.validators import validate_email, validate_password

router = APIRouter()
init_db()

@router.post("/register")
def register(payload: dict):
    if not validate_email(payload.get("email")) or not validate_password(payload.get("password")):
        raise HTTPException(status_code=400, detail="Validation failed")
    token = str(uuid.uuid4())
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO user_mngt_users (email,password,registration_token) VALUES (?,?,?)",
            (payload["email"], payload["password"], token)
        )
        conn.commit()
    except Exception:
        raise HTTPException(status_code=403, detail="User already exists")
    finally:
        conn.close()
    return {"registration_link": f"/api/v1/users/confirm?token={token}"}

@router.get("/confirm")
def confirm(token: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE user_mngt_users SET is_active=1 WHERE registration_token=?", (token,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=400, detail="Invalid token")
    conn.close()
    return {"message": "Registration completed"}
