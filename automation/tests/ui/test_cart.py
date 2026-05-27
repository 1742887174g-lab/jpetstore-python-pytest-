from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from common.config import Settings
from pages.cart_page import CartPage


@allure.epic("JPetStore")
@allure.feature("Cart")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.cart
def test_item_can_be_added_to_cart(page: Page, settings: Settings, test_data: dict) -> None:
    cart_page = CartPage(page, settings.base_url)
    item_id = test_data["catalog"]["item_id"]

    cart_page.add_item(item_id)
    cart_page.assert_item_in_cart(item_id)


@allure.epic("JPetStore")
@allure.feature("Cart")
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.cart
def test_item_quantity_can_be_updated(page: Page, settings: Settings, test_data: dict) -> None:
    cart_page = CartPage(page, settings.base_url)
    item_id = test_data["catalog"]["item_id"]

    cart_page.add_item(item_id)
    cart_page.update_quantity(item_id, 2)
    cart_page.assert_item_in_cart(item_id)
    cart_page.assert_body_contains("$")


@allure.epic("JPetStore")
@allure.feature("Cart")
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.cart
def test_item_can_be_removed_from_cart(page: Page, settings: Settings, test_data: dict) -> None:
    cart_page = CartPage(page, settings.base_url)
    item_id = test_data["catalog"]["item_id"]

    cart_page.add_item(item_id)
    cart_page.remove_item(item_id)
    cart_page.assert_item_not_in_cart(item_id)
