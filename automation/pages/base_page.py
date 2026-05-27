from __future__ import annotations

import re
from urllib.parse import urljoin

from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/") + "/"

    def open(self, path: str = "") -> None:
        self.page.goto(urljoin(self.base_url, path.lstrip("/")))

    def assert_title_contains(self, text: str) -> None:
        expect(self.page).to_have_title(re.compile(re.escape(text), re.IGNORECASE))

    def assert_body_contains(self, text: str) -> None:
        expect(self.page.locator("body")).to_contain_text(text)

    def first_visible(self, selector: str) -> Locator:
        return self.page.locator(selector).locator("visible=true").first()

    def click_link_containing_href(self, href_part: str) -> None:
        self.page.locator(f"a[href*='{href_part}']").first.click()

    def click_submit(self, name: str) -> None:
        self.page.locator(f"input[type='submit'][name='{name}'], button[name='{name}']").first.click()
