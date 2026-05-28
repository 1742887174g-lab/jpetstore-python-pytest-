from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_ALLURE_RESULTS_DIR = PROJECT_ROOT / "reports" / "allure-results"


def build_args(suite: str, headed: bool, allure_results_dir: Path) -> list[str]:
    args = [
        sys.executable,
        "-m",
        "pytest",
        "--alluredir",
        str(allure_results_dir),
    ]
    if suite == "smoke":
        args.extend(["-m", "smoke"])
    elif suite == "ui":
        args.extend(["-m", "ui"])
    elif suite == "api":
        args.extend(["-m", "api"])
    elif suite == "regression":
        args.extend(["-m", "regression"])
    elif suite != "all":
        raise ValueError(f"Unsupported suite: {suite}")

    if headed:
        args.extend(["--headed"])
    return args


def main() -> int:
    parser = argparse.ArgumentParser(description="Run JPetStore automated tests.")
    parser.add_argument("--suite", choices=["smoke", "ui", "api", "regression", "all"], default="smoke")
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--env", help="Environment config name under config/envs.")
    parser.add_argument("--base-url", help="Override JPetStore base URL.")
    parser.add_argument(
        "--allure-results-dir",
        type=Path,
        default=DEFAULT_ALLURE_RESULTS_DIR,
        help="Directory to store Allure raw results.",
    )
    parsed = parser.parse_args()

    command = build_args(parsed.suite, parsed.headed, parsed.allure_results_dir)
    if parsed.env:
        command.extend(["--env", parsed.env])
    if parsed.base_url:
        command.extend(["--base-url", parsed.base_url])
    completed = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
