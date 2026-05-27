from __future__ import annotations

from urllib.parse import urljoin

import allure
import requests


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, path: str, **params: str) -> requests.Response:
        url = urljoin(self.base_url, path.lstrip("/"))
        with allure.step(f"GET {url}"):
            response = self.session.get(url, params=params, timeout=self.timeout)
            allure.attach(
                f"URL: {response.url}\nStatus: {response.status_code}",
                name="api-response-summary",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                response.text[:5000],
                name="api-response-body",
                attachment_type=allure.attachment_type.TEXT,
            )
            return response
