from __future__ import annotations

import logging
from pathlib import Path

from common.config import PROJECT_ROOT, LoggingSettings


def configure_logging(settings: LoggingSettings) -> None:
    log_path = PROJECT_ROOT / settings.file
    log_path.parent.mkdir(parents=True, exist_ok=True)
    level = getattr(logging, settings.level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
