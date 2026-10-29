from collections.abc import Iterator

import pytest
from flask.testing import FlaskClient

from flask_apache import create_app


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    yield create_app().test_client()


@pytest.mark.parametrize("path", ["/", "/health", "/info"])
def test_endpoints_return_json_with_timestamp(client: FlaskClient, path: str) -> None:
    resp = client.get(path)
    assert resp.status_code == 200
    assert resp.is_json and resp.get_json()["timestamp"]


def test_health_is_up(client: FlaskClient) -> None:
    assert client.get("/health").get_json()["status"] == "UP"


def test_info_reports_service(client: FlaskClient) -> None:
    assert client.get("/info").get_json()["service"] == "flask-apache"
