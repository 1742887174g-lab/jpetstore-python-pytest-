from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from common.config import Settings
from pages.home_page import HomePage


@allure.epic("JPetStore")
@allure.feature("Catalog")
@pytest.mark.ui
@pytest.mark.smoke
def test_catalog_page_can_open(page: Page, settings: Settings) -> None:
    home_page = HomePage(page, settings.base_url)
    home_page.open_home()
    home_page.assert_loaded()

