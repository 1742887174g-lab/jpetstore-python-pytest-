from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


SuiteName = Literal["smoke", "ui", "api", "regression", "all"]


class TestRunRequest(BaseModel):
    suite: SuiteName = "smoke"
    environment: str | None = None
    base_url: str | None = None


class TestRunResponse(BaseModel):
    id: int
    suite: SuiteName
    status: Literal["passed", "failed"]
    exit_code: int
    command: str
    environment: str | None = None
    base_url: str | None = None
    started_at: datetime
    finished_at: datetime
    duration_seconds: float
    allure_results_dir: str
    created_at: datetime | None = None


class TestRunDetail(TestRunResponse):
    stdout: str | None = None
    stderr: str | None = None
