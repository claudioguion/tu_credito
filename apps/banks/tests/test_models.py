import pytest
from apps.banks.models import Bank


@pytest.mark.django_db
def test_create_bank():
    bank = Bank.objects.create(
        name="Banco Test",
        type=Bank.Type.PRIVADO,
        address="Main Street 123",
    )

    assert bank.pk is not None
    assert bank.name == "Banco Test"
    assert bank.type == Bank.Type.PRIVADO
