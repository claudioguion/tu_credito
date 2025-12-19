import pytest
from apps.banks.serializers import BankSerializer
from apps.banks.models import Bank


@pytest.mark.django_db
def test_bank_serializer_valid_data():
    data = {
        "name": "Banco Serializado",
        "type": Bank.Type.PRIVADO,
        "address": "Somewhere",
    }

    serializer = BankSerializer(data=data)

    assert serializer.is_valid(), serializer.errors
