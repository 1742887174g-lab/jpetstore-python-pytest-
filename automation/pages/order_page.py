from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class OrderPage(BasePage):
    def fill_payment_and_billing(self, order: dict[str, str]) -> None:
        self.page.locator("select[name='order.cardType']").select_option(order["card_type"])
        self.page.locator("input[name='order.creditCard']").fill(order["card_number"])
        self.page.locator("input[name='order.expiryDate']").fill(order["expiry_date"])
        self.page.locator("input[name='order.billToFirstName']").fill(order["first_name"])
        self.page.locator("input[name='order.billToLastName']").fill(order["last_name"])
        self.page.locator("input[name='order.billAddress1']").fill(order["address1"])
        self.page.locator("input[name='order.billAddress2']").fill(order["address2"])
        self.page.locator("input[name='order.billCity']").fill(order["city"])
        self.page.locator("input[name='order.billState']").fill(order["state"])
        self.page.locator("input[name='order.billZip']").fill(order["zip"])
        self.page.locator("input[name='order.billCountry']").fill(order["country"])

    def continue_order(self) -> None:
        self.page.locator("input[name='newOrder']").click()

    def confirm_order(self) -> None:
        self.page.locator("a[href*='newOrder']").first.click()

    def assert_order_submitted(self) -> None:
        expect(self.page.locator("body")).to_contain_text("Thank you")
