from __future__ import annotations

import re
from urllib.parse import urljoin

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/") + "/"

    def open(self, path: str = "") -> None:
        self.page.goto(urljoin(self.base_url, path.lstrip("/")))

    def assert_title_contains(self, text: str) -> None:
        expect(self.page).to_have_title(re.compile(re.escape(text), re.IGNORECASE))
