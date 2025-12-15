
from fastapi import APIRouter

router = APIRouter()

@router.get("/version")
def version():
    return {"version": "3.0.0"}
