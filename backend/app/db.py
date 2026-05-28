from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "backend" / "data"
DB_PATH = DATA_DIR / "test_platform.db"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS test_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suite TEXT NOT NULL,
                status TEXT NOT NULL,
                exit_code INTEGER NOT NULL,
                command TEXT NOT NULL,
                environment TEXT,
                base_url TEXT,
                started_at TEXT NOT NULL,
                finished_at TEXT NOT NULL,
                duration_seconds REAL NOT NULL,
                run_uid TEXT,
                allure_results_dir TEXT NOT NULL,
                allure_report_dir TEXT,
                allure_report_url TEXT,
                stdout TEXT,
                stderr TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        existing_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(test_runs)").fetchall()
        }
        migrations = {
            "run_uid": "ALTER TABLE test_runs ADD COLUMN run_uid TEXT",
            "allure_report_dir": "ALTER TABLE test_runs ADD COLUMN allure_report_dir TEXT",
            "allure_report_url": "ALTER TABLE test_runs ADD COLUMN allure_report_url TEXT",
        }
        for column, statement in migrations.items():
            if column not in existing_columns:
                connection.execute(statement)


def insert_test_run(record: dict[str, Any]) -> int:
    fields = [
        "suite",
        "status",
        "exit_code",
        "command",
        "environment",
        "base_url",
        "started_at",
        "finished_at",
        "duration_seconds",
        "run_uid",
        "allure_results_dir",
        "allure_report_dir",
        "allure_report_url",
        "stdout",
        "stderr",
        "created_at",
    ]
    placeholders = ", ".join(["?"] * len(fields))
    columns = ", ".join(fields)
    values = [record.get(field) for field in fields]

    with get_connection() as connection:
        cursor = connection.execute(
            f"INSERT INTO test_runs ({columns}) VALUES ({placeholders})",
            values,
        )
        return int(cursor.lastrowid)


def list_test_runs(limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                suite,
                status,
                exit_code,
                command,
                environment,
                base_url,
                started_at,
                finished_at,
                duration_seconds,
                run_uid,
                allure_results_dir,
                allure_report_dir,
                allure_report_url,
                created_at
            FROM test_runs
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()
        return [dict(row) for row in rows]


def get_test_run(run_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM test_runs WHERE id = ?",
            (run_id,),
        ).fetchone()
        return dict(row) if row else None
