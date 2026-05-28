from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

from app.schemas import TestRunRequest, TestRunResponse
from app.db import insert_test_run


REPO_ROOT = Path(__file__).resolve().parents[3]
AUTOMATION_ROOT = REPO_ROOT / "automation"
ALLURE_RESULTS_DIR = AUTOMATION_ROOT / "reports" / "allure-results"


def run_pytest_suite(request: TestRunRequest) -> TestRunResponse:
    started_at = datetime.now()
    command = [
        sys.executable,
        "run_tests.py",
        "--suite",
        request.suite,
    ]
    if request.environment:
        command.extend(["--env", request.environment])
    if request.base_url:
        command.extend(["--base-url", request.base_url])

    completed = subprocess.run(
        command,
        cwd=AUTOMATION_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    finished_at = datetime.now()
    created_at = datetime.now()
    status = "passed" if completed.returncode == 0 else "failed"
    record = {
        "suite": request.suite,
        "status": status,
        "exit_code": completed.returncode,
        "command": " ".join(command),
        "environment": request.environment,
        "base_url": request.base_url,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_seconds": (finished_at - started_at).total_seconds(),
        "allure_results_dir": str(ALLURE_RESULTS_DIR),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "created_at": created_at.isoformat(),
    }
    run_id = insert_test_run(record)

    return TestRunResponse(
        id=run_id,
        suite=request.suite,
        status=status,
        exit_code=completed.returncode,
        command=record["command"],
        environment=request.environment,
        base_url=request.base_url,
        started_at=started_at,
        finished_at=finished_at,
        duration_seconds=(finished_at - started_at).total_seconds(),
        allure_results_dir=str(ALLURE_RESULTS_DIR),
        created_at=created_at,
    )
