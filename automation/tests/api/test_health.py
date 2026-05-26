from __future__ import annotations

import allure
import pytest
import requests

from common.config import Settings


@allure.epic("JPetStore")
@allure.feature("Environment")
@pytest.mark.api
@pytest.mark.smoke
def test_jpetstore_home_is_reachable(settings: Settings) -> None:
    response = requests.get(settings.base_url, timeout=10)
    assert response.status_code < 500

