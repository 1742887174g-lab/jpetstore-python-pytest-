from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


SuiteName = Literal["smoke", "ui", "api", "regression", "all"]


class TestRunRequest(BaseModel):
    suite: SuiteName = "smoke"


class TestRunResponse(BaseModel):
    suite: SuiteName
    status: Literal["passed", "failed"]
    exit_code: int
    started_at: datetime
    finished_at: datetime
    duration_seconds: float
    allure_results_dir: str
