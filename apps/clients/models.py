from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.banks.models import Bank


class Client(models.Model):

    class PersonType(models.TextChoices):
        NATURAL = "NATURAL", "Natural"
        JURIDICO = "JURIDICO", "Juridico"

    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99),
        ],
    )
    nationality = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    email = models.EmailField()
    telephone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    person_type = models.CharField(
        max_length=20,
        choices=PersonType.choices,
    )

    # Foreign
    bank = models.ForeignKey(
        Bank,
        on_delete=models.PROTECT,
        related_name="clients"
    )

    # Extra fields
    document_id = models.CharField(  # Client MUST have valid ID document
        max_length=50,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.document_id
