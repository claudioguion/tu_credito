from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from apps.clients.models import Client
from apps.banks.models import Bank


class Credit(models.Model):

    class CreditType(models.TextChoices):
        AUTOMOTRIZ = "AUTOMOTRIZ", "Automotriz"
        HIPOTECARIO = "HIPOTECARIO", "Hipotecario"
        COMERCIAL = "COMERCIAL", "Comercial"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        CLOSED = "CLOSED", "Closed"

    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255)
    minimum_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    maximum_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    term_months = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    credit_type = models.CharField(
        max_length=20,
        choices=CreditType.choices
    )

    # Foreign
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="credits"
    )
    bank = models.ForeignKey(
        Bank,
        on_delete=models.PROTECT,
        related_name="credits"
    )

    # Extra fields
    status = models.CharField(  # Status for the credit
        max_length=20,
        choices=Status.choices,
        default="PENDING"
    )
    interest_rate = models.DecimalField(  # Bank will probably charge some interest rate
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    registered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-registered_date"]
        verbose_name = "Credit"
        verbose_name_plural = "Credits"

    def clean(self):
        # Let's ensure that the min_pay is <= max_pay 
        if (
            self.minimum_payment is not None
            and self.maximum_payment is not None
            and self.minimum_payment > self.maximum_payment
        ):
            raise ValidationError({
                "minimum_payment": "Minimum payment cannot be greater than maximum payment.",
                "maximum_payment": "Maximum payment must be greater than or equal to minimum payment.",
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.credit_type} - {self.client.full_name}"
