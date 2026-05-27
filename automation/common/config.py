from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yaml"
ENVS_DIR = PROJECT_ROOT / "config" / "envs"


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


class LoggingSettings(BaseModel):
    level: str = "INFO"
    file: str = "reports/logs/automation.log"


class TestUser(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    env: str = "local"
    base_url: str
    browser: BrowserSettings = Field(default_factory=BrowserSettings)
    timeouts: TimeoutSettings = Field(default_factory=TimeoutSettings)
    test_users: dict[str, TestUser] = Field(default_factory=dict)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


@lru_cache
def load_settings(env: str | None = None, base_url: str | None = None) -> Settings:
    raw: dict[str, Any] = yaml.safe_load(SETTINGS_PATH.read_text(encoding="utf-8")) or {}
    env_name = env or raw.get("env", "local")
    env_path = ENVS_DIR / f"{env_name}.yaml"
    if env_path.exists():
        env_raw = yaml.safe_load(env_path.read_text(encoding="utf-8")) or {}
        raw = deep_merge(raw, env_raw)
    if base_url:
        raw["base_url"] = base_url
    return Settings.model_validate(raw)
