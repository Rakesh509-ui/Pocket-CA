from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    user_id: str
    session_id: str
    response: str


class RebuildRequest(BaseModel):
    clear_graph: bool | None = None


class RebuildStatusResponse(BaseModel):
    status: str
    source: str | None = None
    clear_graph: bool | None = None
    job_id: str | None = None
    last_started_at: str | None = None
    last_finished_at: str | None = None
    last_error: str | None = None
    last_summary: dict[str, Any] | None = None


class HealthResponse(BaseModel):
    status: str
    scheduler_enabled: bool
    rebuild: RebuildStatusResponse
