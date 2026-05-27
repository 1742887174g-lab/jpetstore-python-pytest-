from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class AccountPage(BasePage):
    def open_register(self) -> None:
        self.open("actions/Account.action?newAccountForm=")

    def register(self, user: dict[str, str]) -> None:
        self.page.locator("input[name='username']").fill(user["username"])
        self.page.locator("input[name='password']").fill(user["password"])
        self.page.locator("input[name='repeatedPassword']").fill(user["password"])
        self.page.locator("input[name='account.firstName']").fill(user["first_name"])
        self.page.locator("input[name='account.lastName']").fill(user["last_name"])
        self.page.locator("input[name='account.email']").fill(user["email"])
        self.page.locator("input[name='account.phone']").fill(user["phone"])
        self.page.locator("input[name='account.address1']").fill(user["address1"])
        self.page.locator("input[name='account.address2']").fill(user["address2"])
        self.page.locator("input[name='account.city']").fill(user["city"])
        self.page.locator("input[name='account.state']").fill(user["state"])
        self.page.locator("input[name='account.zip']").fill(user["zip"])
        self.page.locator("input[name='account.country']").fill(user["country"])
        self.page.locator("select[name='account.languagePreference']").select_option(user["language"])
        self.page.locator("select[name='account.favouriteCategoryId']").select_option(user["favourite_category"])
        self.page.locator("input[name='newAccount']").click()

    def assert_registered(self) -> None:
        expect(self.page.get_by_role("link", name="Sign In")).to_be_visible()
