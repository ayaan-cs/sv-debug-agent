"""Thin FastAPI wrapper around sv_debug. No debugging logic lives here."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

APP_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = APP_DIR.parent.parent
DIST = APP_DIR / "frontend" / "dist"

for path in (REPO_ROOT, APP_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from sv_debug import (  # noqa: E402
    SAMPLES,
    debug_systemverilog,
    demo_mode_enabled,
    has_api_key,
    suggest_alternatives,
)

app = FastAPI(
    title="SV Debug Agent API",
    description="Local API for the SV Debug Agent UI. Debugging logic lives in sv_debug/.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://127.0.0.1:8765",
        "http://localhost:8765",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DebugRequest(BaseModel):
    input: str = Field(..., min_length=1)


class AlternativeModel(BaseModel):
    title: str
    code: str
    note: str = ""


class DebugResponse(BaseModel):
    result: str
    demo_mode: bool
    alternatives: list[AlternativeModel] = []


class StatusResponse(BaseModel):
    demo_mode: bool
    has_api_key: bool
    app_name: str = "SV Debug Agent"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/status", response_model=StatusResponse)
def status() -> StatusResponse:
    return StatusResponse(
        demo_mode=demo_mode_enabled(),
        has_api_key=has_api_key(),
    )


@app.get("/api/samples")
def samples() -> list[dict[str, str]]:
    return SAMPLES


@app.post("/api/debug", response_model=DebugResponse)
def debug(body: DebugRequest) -> DebugResponse:
    text = body.input.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Paste SystemVerilog code or an error first.")

    try:
        # UI renders structured alternatives separately — avoid duplicate markdown blocks.
        result = debug_systemverilog(text, include_alternatives_markdown=False)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Debug failed: {exc}") from exc

    alts: list[AlternativeModel] = []
    if demo_mode_enabled():
        alts = [AlternativeModel(**item) for item in suggest_alternatives(text)]

    return DebugResponse(
        result=result,
        demo_mode=demo_mode_enabled(),
        alternatives=alts,
    )


# Serve the built React UI for the desktop app / single-server mode.
# API routes above take precedence; this must stay last.
if DIST.exists():
    app.mount("/", StaticFiles(directory=DIST, html=True), name="ui")
