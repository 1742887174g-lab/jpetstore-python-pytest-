from __future__ import annotations

from uuid import uuid4

import allure
import pytest
from playwright.sync_api import Page

from common.config import Settings
from pages.account_page import AccountPage


def build_unique_user(test_data: dict) -> dict[str, str]:
    template = test_data["new_user"]
    suffix = uuid4().hex[:8]
    username = f"{template['username_prefix']}{suffix}"
    return {
        **template,
        "username": username,
        "email": f"{username}@{template['email_domain']}",
    }


@allure.epic("JPetStore")
@allure.feature("Account")
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.account
def test_new_user_can_register(page: Page, settings: Settings, test_data: dict) -> None:
    account_page = AccountPage(page, settings.base_url)
    new_user = build_unique_user(test_data)

    account_page.open_register()
    account_page.register(new_user)
    account_page.assert_registered()
