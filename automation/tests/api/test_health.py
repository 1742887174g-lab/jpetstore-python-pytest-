from __future__ import annotations

import allure
import pytest

from common.api_client import ApiClient
from common.config import Settings


@allure.epic("JPetStore")
@allure.feature("Environment")
@pytest.mark.api
@pytest.mark.smoke
def test_jpetstore_home_is_reachable(settings: Settings) -> None:
    client = ApiClient(settings.base_url)
    response = client.get("")
    assert response.status_code < 500


@allure.epic("JPetStore")
@allure.feature("Catalog API")
@pytest.mark.api
@pytest.mark.smoke
def test_catalog_action_is_reachable(settings: Settings) -> None:
    client = ApiClient(settings.base_url)
    response = client.get("actions/Catalog.action")
    assert response.status_code == 200
    assert "JPetStore" in response.text


@allure.epic("JPetStore")
@allure.feature("Catalog API")
@pytest.mark.api
@pytest.mark.regression
def test_product_search_endpoint_returns_results(settings: Settings, test_data: dict) -> None:
    client = ApiClient(settings.base_url)
    response = client.get(
        "actions/Catalog.action",
        searchProducts="",
        keyword=test_data["catalog"]["keyword"],
    )
    assert response.status_code == 200
    assert test_data["catalog"]["keyword"].lower() in response.text.lower()
