from __future__ import annotations

from pathlib import Path

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from common.config import PROJECT_ROOT, Settings, load_settings


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--headed", action="store_true", help="Run browser tests in headed mode.")


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session")
def browser(settings: Settings, pytestconfig: pytest.Config) -> Browser:
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, settings.browser.name)
        headed = pytestconfig.getoption("--headed")
        browser = browser_type.launch(
            headless=False if headed else settings.browser.headless,
            slow_mo=settings.browser.slow_mo_ms,
        )
        yield browser
        browser.close()


@pytest.fixture()
def context(browser: Browser, settings: Settings) -> BrowserContext:
    context = browser.new_context(
        viewport={
            "width": settings.browser.viewport.width,
            "height": settings.browser.viewport.height,
        }
    )
    context.set_default_timeout(settings.timeouts.default_ms)
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    screenshot_dir = PROJECT_ROOT / "reports" / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"{item.name}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
    allure.attach.file(
        str(screenshot_path),
        name="failure-screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
