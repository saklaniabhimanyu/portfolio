from fastapi import APIRouter
from backend.services import data_service

router = APIRouter()


@router.get("/api/profile")
def read_profile():
    return data_service.get_profile()
