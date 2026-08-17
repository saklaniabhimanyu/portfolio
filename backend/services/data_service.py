"""
Loads the portfolio's JSON data files from /data.
Kept intentionally simple: no database, since a handful of JSON files
is all this content needs. Swap this module for a real DB-backed
service later without touching the routes.

Not cached: these files are tiny (a few KB) and read on every request,
so edits to the JSON show up immediately without restarting the server.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def _load(filename: str):
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_profile():
    return _load("profile.json")


def get_experience():
    return _load("experience.json")


def get_education():
    return _load("education.json")


def get_projects():
    return _load("projects.json")


def get_academic_projects():
    return _load("academic_projects.json")


def get_project_by_id(project_id: str):
    for project in get_projects() + get_academic_projects():
        if project["id"] == project_id:
            return project
    return None


def get_skills():
    return _load("skills.json")


def get_achievements():
    return _load("achievements.json")
