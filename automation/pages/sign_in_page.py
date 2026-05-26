from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class SignInPage(BasePage):
    def login(self, username: str, password: str) -> None:
        self.page.locator("input[name='username']").fill(username)
        self.page.locator("input[name='password']").fill(password)
        self.page.locator("input[name='signon']").click()

    def assert_login_success(self) -> None:
        expect(self.page.locator("body")).to_contain_text("Welcome")

