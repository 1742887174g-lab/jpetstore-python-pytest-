from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class SignInPage(BasePage):
    def open_sign_in(self) -> None:
        self.open("actions/Account.action?signonForm=")

    def login(self, username: str, password: str) -> None:
        self.page.locator("input[name='username']").fill(username)
        self.page.locator("input[name='password']").fill(password)
        self.page.locator("input[name='signon']").click()

    def assert_login_success(self) -> None:
        expect(self.page.locator("body")).to_contain_text("Welcome")

    def assert_login_failed(self) -> None:
        expect(self.page.locator("body")).to_contain_text("Invalid username or password")

    def sign_out(self) -> None:
        self.page.get_by_role("link", name="Sign Out").click()

    def assert_signed_out(self) -> None:
        expect(self.page.get_by_role("link", name="Sign In")).to_be_visible()
