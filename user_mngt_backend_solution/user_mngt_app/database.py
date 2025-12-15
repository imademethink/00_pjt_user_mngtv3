import sqlite3
import os
import logging

logger = logging.getLogger("user_mngt.database")

DB_DIR = "/app/user_mngt_data"
DB_PATH = os.path.join(DB_DIR, "user_mngt_db.sqlite")


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def _column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Base table (never dropped)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_mngt_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_active INTEGER DEFAULT 0,
            registration_token TEXT,
            otp TEXT,
            session_key TEXT,
            first_name TEXT,
            last_name TEXT,
            address1 TEXT,
            address2 TEXT,
            city TEXT,
            state TEXT,
            country TEXT,
            pin_code TEXT,
            contact_country_code TEXT,
            contact_number TEXT
        )
    """)

    # Add login-attempt related columns safely
    if not _column_exists(cur, "user_mngt_users", "failed_login_attempts"):
        logger.debug("Adding column failed_login_attempts")
        cur.execute(
            "ALTER TABLE user_mngt_users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0"
        )

    if not _column_exists(cur, "user_mngt_users", "lock_until"):
        logger.debug("Adding column lock_until")
        cur.execute(
            "ALTER TABLE user_mngt_users ADD COLUMN lock_until TEXT"
        )

    conn.commit()
    conn.close()
