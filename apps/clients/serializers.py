from rest_framework import serializers
from datetime import date

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source="bank.name", read_only=True)

    class Meta:
        model = Client
        exclude = [
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        birth_date = data.get("birth_date")
        age = data.get("age")

        if birth_date and age is not None:
            today = date.today()
            expected_age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )
            if age != expected_age:
                raise serializers.ValidationError(
                    {"age": f"Age ({age}) does not match birth_date ({birth_date})"}
                )
        return data
