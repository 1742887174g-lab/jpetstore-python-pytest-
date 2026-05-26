from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

from app.schemas import TestRunRequest, TestRunResponse


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
    completed = subprocess.run(command, cwd=AUTOMATION_ROOT, check=False)
    finished_at = datetime.now()

    return TestRunResponse(
        suite=request.suite,
        status="passed" if completed.returncode == 0 else "failed",
        exit_code=completed.returncode,
        started_at=started_at,
        finished_at=finished_at,
        duration_seconds=(finished_at - started_at).total_seconds(),
        allure_results_dir=str(ALLURE_RESULTS_DIR),
    )

