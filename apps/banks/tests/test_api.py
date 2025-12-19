import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.banks.models import Bank


@pytest.mark.django_db
def test_list_banks_no_auth():
    Bank.objects.create(name="Banco A", type=Bank.Type.PRIVADO)
    Bank.objects.create(name="Banco B", type=Bank.Type.GOBIERNO)

    client = APIClient()
    response = client.get("/api/bancos/")

    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_create_bank_authenticated():
    User = get_user_model()
    user = User.objects.create_user(
        email="test@example.com",
        password="pass1234"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/bancos/",
        {
            "name": "Banco Privado",
            "type": Bank.Type.PRIVADO,
        },
        format="json",
    )

    assert response.status_code == 201
    assert Bank.objects.count() == 1


@pytest.mark.django_db
def test_filter_banks_by_type():
    Bank.objects.create(name="Banco Privado", type=Bank.Type.PRIVADO)
    Bank.objects.create(name="Banco Gobierno", type=Bank.Type.GOBIERNO)

    client = APIClient()
    response = client.get("/api/bancos/?type=PRIVADO")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["type"] == "PRIVADO"


@pytest.mark.django_db
def test_pagination_default_limit():
    for i in range(15):
        Bank.objects.create(name=f"Banco {i}", type=Bank.Type.PRIVADO)

    client = APIClient()
    response = client.get("/api/bancos/")

    assert response.status_code == 200
    assert len(response.data["results"]) <= 10
