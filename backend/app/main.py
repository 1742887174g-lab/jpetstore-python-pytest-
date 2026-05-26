from __future__ import annotations

from fastapi import FastAPI

from app.schemas import TestRunRequest, TestRunResponse
from app.services.test_runner import run_pytest_suite


app = FastAPI(title="JPetStore Test Platform API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/test-runs", response_model=TestRunResponse)
def create_test_run(request: TestRunRequest) -> TestRunResponse:
    return run_pytest_suite(request)

