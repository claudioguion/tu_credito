from rest_framework.test import APIClient


def test_api_security_headers_present(db):
    client = APIClient()
    response = client.get("/api/bancos/")

    assert "Content-Security-Policy" in response.headers
    assert "Permissions-Policy" in response.headers


def test_admin_no_security_headers(db):
    client = APIClient()
    response = client.get("/admin/login/")

    assert "Content-Security-Policy" not in response.headers

