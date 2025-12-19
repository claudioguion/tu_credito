from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        # Can't escalate privileges through this endpoint. Only by Django Admin
        user.is_staff = False
        user.is_superuser = False

        # For role/status fields:
        if hasattr(user, "role"):
            user.role = "user"

        if hasattr(user, "status"):
            user.status = "active"

        user.save()
        return user
