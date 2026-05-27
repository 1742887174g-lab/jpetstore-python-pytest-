from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class CatalogPage(BasePage):
    def open_catalog(self) -> None:
        self.open("actions/Catalog.action")

    def assert_loaded(self) -> None:
        expect(self.page.get_by_role("link", name="Sign In")).to_be_visible()
        expect(self.page.locator("input[name='keyword']")).to_be_visible()

    def open_category(self, category_id: str) -> None:
        self.open(f"actions/Catalog.action?viewCategory=&categoryId={category_id}")

    def open_product(self, product_id: str) -> None:
        self.open(f"actions/Catalog.action?viewProduct=&productId={product_id}")

    def open_item(self, item_id: str) -> None:
        self.open(f"actions/Catalog.action?viewItem=&itemId={item_id}")

    def search(self, keyword: str) -> None:
        self.page.locator("input[name='keyword']").fill(keyword)
        self.page.locator("input[name='searchProducts']").click()

    def assert_search_results(self, keyword: str) -> None:
        expect(self.page.locator("body")).to_contain_text(keyword, ignore_case=True)

    def assert_product_visible(self, product_id: str) -> None:
        expect(self.page.locator("body")).to_contain_text(product_id)

    def add_item_to_cart(self, item_id: str) -> None:
        self.open_item(item_id)
        self.page.locator("a[href*='addItemToCart']").first.click()

    def assert_item_visible(self, item_id: str) -> None:
        expect(self.page.locator("body")).to_contain_text(item_id)
