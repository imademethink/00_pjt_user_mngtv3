
from fastapi import FastAPI
import logging
from user_mngt_app.routers import users, auth, profile, version, v3

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="User Management API", version="3.0.0")

app.include_router(users.router, prefix="/api/v1/users")
app.include_router(auth.router, prefix="/api/v1/users")
app.include_router(profile.router, prefix="/api/v1")
app.include_router(v3.router, prefix="/api/v3/users")
app.include_router(version.router, prefix="/api/v1")
