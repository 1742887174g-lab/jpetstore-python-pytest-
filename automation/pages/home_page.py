from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    def open_home(self) -> None:
        self.open("actions/Catalog.action")

    def assert_loaded(self) -> None:
        expect(self.page.get_by_role("link", name="Sign In")).to_be_visible()
        expect(self.page.locator("input[name='keyword']")).to_be_visible()

    def go_to_sign_in(self) -> None:
        self.page.get_by_role("link", name="Sign In").click()

    def go_to_register(self) -> None:
        self.go_to_sign_in()
        self.page.get_by_role("link", name="Register Now!").click()
