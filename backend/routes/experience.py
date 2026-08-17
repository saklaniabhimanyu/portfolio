from fastapi import APIRouter
from backend.services import data_service

router = APIRouter()


@router.get("/api/experience")
def read_experience():
    return data_service.get_experience()
