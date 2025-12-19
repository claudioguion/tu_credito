import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.banks.models import Bank
from apps.clients.models import Client
from apps.credits.models import Credit

pytestmark = pytest.mark.django_db  # all tests will use the test DB


# Fixtures
@pytest.fixture
def auth_client():
    User = get_user_model()
    user = User.objects.create_user(email="test@example.com", password="pass1234")
    client = APIClient()
    # JWT token
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.fixture
def banks():
    b1 = Bank.objects.create(name="Banco A", type=Bank.Type.PRIVADO, address="123 Main St")
    b2 = Bank.objects.create(name="Banco B", type=Bank.Type.GOBIERNO, address="456 Second St")
    return b1, b2


@pytest.fixture
def clients(banks):
    b1, b2 = banks
    c1 = Client.objects.create(
        full_name="John Doe",
        birth_date="1990-01-01",
        age=35,
        nationality="US",
        address="123 Main St",
        email="john@example.com",
        person_type=Client.PersonType.NATURAL,
        bank=b1,
        document_id="JD001"
    )
    c2 = Client.objects.create(
        full_name="Jane Smith",
        birth_date="1985-05-05",
        age=40,
        nationality="US",
        address="456 Second St",
        email="jane@example.com",
        person_type=Client.PersonType.JURIDICO,
        bank=b2,
        document_id="JS002"
    )
    return c1, c2


@pytest.fixture
def credits(clients, banks):
    c1, c2 = clients
    b1, b2 = banks
    cr1 = Credit.objects.create(
        client=c1,
        description="Auto Loan",
        minimum_payment=500,
        maximum_payment=2000,
        term_months=24,
        bank=b1,
        credit_type=Credit.CreditType.AUTOMOTRIZ
    )
    cr2 = Credit.objects.create(
        client=c2,
        description="Mortgage",
        minimum_payment=1000,
        maximum_payment=5000,
        term_months=120,
        bank=b2,
        credit_type=Credit.CreditType.HIPOTECARIO
    )
    return cr1, cr2


# API tests
def test_list_credits_no_auth(credits):
    client = APIClient()
    response = client.get("/api/creditos/", follow=True)
    assert response.status_code == 200
    assert len(response.data["results"]) == 2


def test_create_credit_auth(auth_client, clients, banks):
    c1, _ = clients
    b1, _ = banks
    response = auth_client.post(
        "/api/creditos/",
        {
            "client": c1.id,
            "description": "Personal Loan",
            "minimum_payment": 300,
            "maximum_payment": 1500,
            "term_months": 12,
            "bank": b1.id,
            "credit_type": "COMERCIAL"
        },
        format="json"
    )
    assert response.status_code == 201
    from apps.credits.models import Credit
    assert Credit.objects.filter(description="Personal Loan").exists()


def test_filter_credits_by_bank(credits, banks):
    client = APIClient()
    b1, b2 = banks
    response = client.get(f"/api/creditos/?bank={b2.id}", follow=True)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["bank_name"] == "Banco B"


def test_filter_credits_by_credit_type(credits):
    client = APIClient()
    response = client.get("/api/creditos/?credit_type=AUTOMOTRIZ", follow=True)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["credit_type"] == "AUTOMOTRIZ"


def test_search_credits_by_description(credits):
    client = APIClient()
    response = client.get("/api/creditos/?search=Auto", follow=True)
    assert response.status_code == 200
    assert response.data["results"][0]["description"] == "Auto Loan"


def test_pagination_credits(credits, clients, banks):
    c1, _ = clients
    b1, _ = banks
    # create extra credits for pagination
    for i in range(15):
        Credit.objects.create(
            client=c1,
            description=f"Credit {i}",
            minimum_payment=100 + i,
            maximum_payment=500 + i,
            term_months=12,
            bank=b1,
            credit_type=Credit.CreditType.COMERCIAL
        )
    client_api = APIClient()
    response = client_api.get("/api/creditos/?page=1&page_size=10", follow=True)
    assert response.status_code == 200
    assert len(response.data["results"]) == 10
