"""
Reads the portfolio JSON data directly from /data for the Streamlit app.

Kept separate from the FastAPI backend on purpose: Streamlit apps are
usually deployed as a single process (e.g. Streamlit Community Cloud),
so the frontend shouldn't depend on a second running server just to
render. The FastAPI backend in /backend exposes the same data over
REST for any other client that wants it.
"""
import json
from pathlib import Path
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def _load_json_cached(filename: str, _mtime: float):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json(filename: str):
    """Cache keyed on (filename, mtime) so editing a JSON file is picked up
    on the next rerun -- a plain st.cache_data on filename alone would keep
    serving the old content until the server process itself restarts."""
    mtime = (DATA_DIR / filename).stat().st_mtime
    return _load_json_cached(filename, mtime)


def get_profile():
    return load_json("profile.json")


def get_experience():
    return load_json("experience.json")


def get_education():
    return load_json("education.json")


def get_projects():
    return load_json("projects.json")


def get_academic_projects():
    return load_json("academic_projects.json")


def get_project(project_id: str):
    for p in get_projects() + get_academic_projects():
        if p["id"] == project_id:
            return p
    return None


def get_skills():
    return load_json("skills.json")


def get_achievements():
    return load_json("achievements.json")
