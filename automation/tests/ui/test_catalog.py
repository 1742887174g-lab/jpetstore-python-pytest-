from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from common.config import Settings
from pages.catalog_page import CatalogPage


@allure.epic("JPetStore")
@allure.feature("Catalog")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.catalog
def test_catalog_page_can_open(page: Page, settings: Settings) -> None:
    catalog_page = CatalogPage(page, settings.base_url)

    catalog_page.open_catalog()
    catalog_page.assert_loaded()


@allure.epic("JPetStore")
@allure.feature("Catalog")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.catalog
def test_search_products_by_keyword(page: Page, settings: Settings, test_data: dict) -> None:
    catalog_page = CatalogPage(page, settings.base_url)
    keyword = test_data["catalog"]["keyword"]

    catalog_page.open_catalog()
    catalog_page.search(keyword)
    catalog_page.assert_search_results(keyword)


@allure.epic("JPetStore")
@allure.feature("Catalog")
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.catalog
def test_product_detail_can_open(page: Page, settings: Settings, test_data: dict) -> None:
    catalog_page = CatalogPage(page, settings.base_url)
    product_id = test_data["catalog"]["product_id"]

    catalog_page.open_product(product_id)
    catalog_page.assert_product_visible(product_id)
