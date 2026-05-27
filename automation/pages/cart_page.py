from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class CartPage(BasePage):
    def open_cart(self) -> None:
        self.open("actions/Cart.action?viewCart=")

    def add_item(self, item_id: str) -> None:
        self.open(f"actions/Cart.action?addItemToCart=&workingItemId={item_id}")

    def update_quantity(self, item_id: str, quantity: int) -> None:
        self.page.locator(f"input[name='{item_id}']").fill(str(quantity))
        self.page.locator("input[name='updateCartQuantities']").click()

    def remove_item(self, item_id: str) -> None:
        self.page.locator(f"a[href*='removeItemFromCart'][href*='{item_id}']").first.click()

    def proceed_to_checkout(self) -> None:
        self.page.locator("a[href*='newOrderForm']").first.click()

    def assert_item_in_cart(self, item_id: str) -> None:
        expect(self.page.locator("body")).to_contain_text(item_id)

    def assert_item_not_in_cart(self, item_id: str) -> None:
        expect(self.page.locator("body")).not_to_contain_text(item_id)

    def assert_cart_empty(self) -> None:
        expect(self.page.locator("body")).to_contain_text("Your cart is empty")
