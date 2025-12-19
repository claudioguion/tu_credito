from django.db import models


class Bank(models.Model):

    class Type(models.TextChoices):
        PRIVADO = "PRIVADO", "Privado"
        GOBIERNO = "GOBIERNO", "Gobierno"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    
    # Extra fields
    code = models.CharField(  # Bank should have it's own identifier/code/reference for inter-bank operations
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )
    contact_email = models.EmailField(
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Bank"
        verbose_name_plural = "Banks"

    def __str__(self):
        return self.name
