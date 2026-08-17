"""
FastAPI backend for Abhimanyu Saklani's portfolio.

Run with:
    uvicorn backend.main:app --reload --port 8000

This backend is optional for the Streamlit site itself — the frontend
reads /data/*.json directly for speed and zero-config deployment — but
it's here so the same content can be consumed by any other client
(a future React rewrite, a CLI, a resume-bot, etc.) over a clean REST API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import profile, projects, experience, education

app = FastAPI(
    title="Abhimanyu Saklani — Portfolio API",
    description="Read-only API exposing profile, experience, education, projects, skills, and achievements.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(profile.router, tags=["profile"])
app.include_router(projects.router, tags=["projects"])
app.include_router(experience.router, tags=["experience"])
app.include_router(education.router, tags=["education"])


@app.get("/")
def root():
    return {"status": "ok", "message": "Portfolio API — see /docs for endpoints."}
