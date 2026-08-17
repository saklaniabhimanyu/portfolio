from fastapi import APIRouter
from backend.services import data_service

router = APIRouter()


@router.get("/api/education")
def read_education():
    return data_service.get_education()


@router.get("/api/skills")
def read_skills():
    return data_service.get_skills()


@router.get("/api/achievements")
def read_achievements():
    return data_service.get_achievements()
