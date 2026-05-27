from __future__ import annotations

from functools import lru_cache
from typing import Any

import yaml

from common.config import PROJECT_ROOT


TEST_DATA_PATH = PROJECT_ROOT / "testdata" / "jpetstore_data.yaml"


@lru_cache
def load_test_data() -> dict[str, Any]:
    return yaml.safe_load(TEST_DATA_PATH.read_text(encoding="utf-8")) or {}
