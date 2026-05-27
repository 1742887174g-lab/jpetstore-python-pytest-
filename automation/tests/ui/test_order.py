from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from common.config import Settings
from pages.cart_page import CartPage
from pages.order_page import OrderPage
from pages.sign_in_page import SignInPage


@allure.epic("JPetStore")
@allure.feature("Order")
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.order
def test_default_user_can_submit_order(page: Page, settings: Settings, test_data: dict) -> None:
    user = settings.test_users["default"]
    item_id = test_data["catalog"]["item_id"]
    order_data = test_data["order"]
    sign_in_page = SignInPage(page, settings.base_url)
    cart_page = CartPage(page, settings.base_url)
    order_page = OrderPage(page, settings.base_url)

    sign_in_page.open_sign_in()
    sign_in_page.login(user.username, user.password)
    sign_in_page.assert_login_success()
    cart_page.add_item(item_id)
    cart_page.proceed_to_checkout()
    order_page.fill_payment_and_billing(order_data)
    order_page.continue_order()
    order_page.confirm_order()
    order_page.assert_order_submitted()
