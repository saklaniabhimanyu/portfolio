from fastapi import APIRouter, HTTPException
from backend.services import data_service

router = APIRouter()


@router.get("/api/projects")
def read_projects():
    return data_service.get_projects()


@router.get("/api/academic-projects")
def read_academic_projects():
    return data_service.get_academic_projects()


@router.get("/api/projects/{project_id}")
def read_project(project_id: str):
    project = data_service.get_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
