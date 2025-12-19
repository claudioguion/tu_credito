from decimal import Decimal
from rest_framework import serializers
from .models import Credit


class CreditSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.full_name", read_only=True)
    bank_name = serializers.CharField(source="bank.name", read_only=True)

    # Use Decimal for min_value to avoid DRF warnings
    minimum_payment = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.00")
    )
    maximum_payment = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01")
    )

    class Meta:
        model = Credit
        exclude = ["updated_at"]

    def validate(self, data):
        min_payment = data.get("minimum_payment")
        max_payment = data.get("maximum_payment")
        if min_payment and max_payment and min_payment > max_payment:
            raise serializers.ValidationError("Minimum payment cannot exceed maximum payment.")
        return data
