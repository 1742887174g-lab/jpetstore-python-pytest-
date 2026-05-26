from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from common.config import Settings
from pages.home_page import HomePage
from pages.sign_in_page import SignInPage


@allure.epic("JPetStore")
@allure.feature("Sign In")
@pytest.mark.ui
@pytest.mark.smoke
def test_default_user_can_sign_in(page: Page, settings: Settings) -> None:
    user = settings.test_users["default"]
    home_page = HomePage(page, settings.base_url)
    sign_in_page = SignInPage(page, settings.base_url)

    home_page.open_home()
    home_page.go_to_sign_in()
    sign_in_page.login(user.username, user.password)
    sign_in_page.assert_login_success()

