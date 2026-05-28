from __future__ import annotations

import subprocess
import sys
import shutil
from datetime import datetime
from pathlib import Path

from app.db import insert_test_run
from app.schemas import TestRunRequest, TestRunResponse


REPO_ROOT = Path(__file__).resolve().parents[3]
AUTOMATION_ROOT = REPO_ROOT / "automation"
RUNS_ROOT = AUTOMATION_ROOT / "reports" / "runs"
ALLURE_COMMAND = REPO_ROOT / "allure.cmd"


def build_run_uid(suite: str, started_at: datetime) -> str:
    timestamp = started_at.strftime("%Y%m%d_%H%M%S_%f")
    return f"{timestamp}_{suite}"


def generate_allure_report(results_dir: Path, report_dir: Path) -> tuple[bool, str, str]:
    if not results_dir.exists() or not any(results_dir.iterdir()):
        return False, "", "Allure results directory is empty."

    command = [
        str(ALLURE_COMMAND if ALLURE_COMMAND.exists() else "allure"),
        "generate",
        str(results_dir),
        "-o",
        str(report_dir),
        "--clean",
    ]
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.returncode == 0, completed.stdout, completed.stderr


def run_pytest_suite(request: TestRunRequest) -> TestRunResponse:
    started_at = datetime.now()
    run_uid = build_run_uid(request.suite, started_at)
    run_root = RUNS_ROOT / run_uid
    allure_results_dir = run_root / "allure-results"
    allure_report_dir = run_root / "allure-report"
    if run_root.exists():
        shutil.rmtree(run_root)
    allure_results_dir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "run_tests.py",
        "--suite",
        request.suite,
        "--allure-results-dir",
        str(allure_results_dir),
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
    report_generated, report_stdout, report_stderr = generate_allure_report(
        allure_results_dir,
        allure_report_dir,
    )
    allure_report_url = f"/reports/{run_uid}/allure-report/index.html" if report_generated else None
    stdout = completed.stdout
    stderr = completed.stderr
    if report_stdout:
        stdout = f"{stdout}\n\n[allure generate stdout]\n{report_stdout}"
    if report_stderr:
        stderr = f"{stderr}\n\n[allure generate stderr]\n{report_stderr}"

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
        "run_uid": run_uid,
        "allure_results_dir": str(allure_results_dir),
        "allure_report_dir": str(allure_report_dir) if report_generated else None,
        "allure_report_url": allure_report_url,
        "stdout": stdout,
        "stderr": stderr,
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
        run_uid=run_uid,
        started_at=started_at,
        finished_at=finished_at,
        duration_seconds=(finished_at - started_at).total_seconds(),
        allure_results_dir=str(allure_results_dir),
        allure_report_dir=record["allure_report_dir"],
        allure_report_url=allure_report_url,
        created_at=created_at,
    )
