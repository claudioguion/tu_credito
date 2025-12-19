import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.banks.models import Bank
from apps.clients.models import Client
from apps.clients.serializers import ClientSerializer

pytestmark = pytest.mark.django_db  # enable DB for all tests in this file


# Fixtures
@pytest.fixture
def auth_client():
    User = get_user_model()
    user = User.objects.create_user(email="test@example.com", password="pass1234")
    client = APIClient()
    client.force_authenticate(user=user)
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
        document_id="C1_Z",
        bank=b1
    )
    c2 = Client.objects.create(
        full_name="Jane Smith",
        birth_date="1985-05-05",
        age=40,
        nationality="US",
        address="456 Second St",
        email="jane@example.com",
        person_type=Client.PersonType.JURIDICO,
        document_id="C2_Y",
        bank=b2
    )
    return c1, c2


# Model tests
def test_client_model(clients, banks):
    c1, c2 = clients
    b1, b2 = banks
    assert c1.bank == b1
    assert c2.bank == b2
    assert c1.address == "123 Main St"
    assert c2.nationality == "US"


# Serializer tests
def test_client_serializer(clients):
    c1, _ = clients
    serializer = ClientSerializer(c1)
    data = serializer.data
    assert data["full_name"] == "John Doe"
    assert data["bank_name"] == "Banco A"
    assert data["address"] == "123 Main St"
    assert data["nationality"] == "US"


# API tests
def test_list_clients_no_auth(clients):
    client = APIClient()
    response = client.get("/api/clientes/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 2


def test_create_client_auth(auth_client, banks):
    b1, _ = banks
    response = auth_client.post(
        "/api/clientes/",
        {
            "full_name": "New Client",
            "birth_date": "1992-02-02",
            "age": 33,
            "nationality": "US",
            "address": "789 Third St",
            "email": "new@example.com",
            "person_type": Client.PersonType.NATURAL,
            "document_id": "assert_create_client_auth123",
            "bank": b1.id
        },
        format="json"
    )
    assert response.status_code == 201
    assert Client.objects.filter(email="new@example.com").exists()


def test_filter_clients_by_person_type(clients):
    client = APIClient()
    response = client.get("/api/clientes/?person_type=NATURAL")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["person_type"] == "NATURAL"


def test_filter_clients_by_bank_name(clients):
    client = APIClient()
    response = client.get("/api/clientes/?bank_name=Banco B")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["bank_name"] == "Banco B"


def test_search_clients_by_name(clients):
    client = APIClient()
    response = client.get("/api/clientes/?search=Jane")
    assert response.status_code == 200
    assert response.data["results"][0]["full_name"] == "Jane Smith"


def test_pagination_clients(clients, banks):
    b1, _ = banks
    # create extra clients for pagination
    for i in range(15):
        Client.objects.create(
            full_name=f"Client {i}",
            birth_date="1990-01-01",
            age=30+i,
            nationality="US",
            address=f"{i} Example St",
            email=f"{i}@example.com",
            person_type=Client.PersonType.NATURAL,
            document_id=f"pagination_{i}",
            bank=b1
        )
    client = APIClient()
    response = client.get("/api/clientes/?page=1&page_size=10")
    assert response.status_code == 200
    assert len(response.data["results"]) == 10
