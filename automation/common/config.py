from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yaml"


class Viewport(BaseModel):
    width: int = 1366
    height: int = 768


class BrowserSettings(BaseModel):
    name: str = "chromium"
    headless: bool = True
    slow_mo_ms: int = 0
    viewport: Viewport = Field(default_factory=Viewport)


class TimeoutSettings(BaseModel):
    default_ms: int = 10000


class TestUser(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    env: str = "local"
    base_url: str
    browser: BrowserSettings = Field(default_factory=BrowserSettings)
    timeouts: TimeoutSettings = Field(default_factory=TimeoutSettings)
    test_users: dict[str, TestUser] = Field(default_factory=dict)


@lru_cache
def load_settings() -> Settings:
    raw: dict[str, Any] = yaml.safe_load(SETTINGS_PATH.read_text(encoding="utf-8"))
    return Settings.model_validate(raw)

