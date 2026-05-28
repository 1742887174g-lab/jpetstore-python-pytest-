from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import get_test_run, init_db, list_test_runs
from app.schemas import TestRunDetail, TestRunRequest, TestRunResponse
from app.services.test_runner import run_pytest_suite


app = FastAPI(title="JPetStore Test Platform API")
REPO_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = REPO_ROOT / "automation" / "reports" / "runs"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/reports", StaticFiles(directory=REPORTS_DIR), name="reports")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/test-runs", response_model=TestRunResponse)
def create_test_run(request: TestRunRequest) -> TestRunResponse:
    return run_pytest_suite(request)


@app.get("/test-runs", response_model=list[TestRunResponse])
def get_test_runs(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[dict]:
    return list_test_runs(limit=limit, offset=offset)


@app.get("/test-runs/{run_id}", response_model=TestRunDetail)
def get_test_run_detail(run_id: int) -> dict:
    record = get_test_run(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Test run not found")
    return record
