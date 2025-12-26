from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from pages.models import Project

User = get_user_model()


class Payment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_payments"
    )

    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="freelancer_payments"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    admin_commission_percent = models.PositiveIntegerField(
        default=20
    )

    admin_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    freelancer_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed')
        ],
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "freelancer"],
                name="unique_payment_per_project_freelancer"
            )
        ]

    # ✅ THIS IS WHERE THE LOGIC GOES
    def save(self, *args, **kwargs):
        self.admin_amount = (
            self.total_amount * Decimal(self.admin_commission_percent) / Decimal("100")
        )
        self.freelancer_amount = self.total_amount - self.admin_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment #{self.id} - {self.total_amount}"



class Review(models.Model):
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name="review"
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client_reviews"
    )

    freelancer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="freelancer_reviews"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    feedback = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        if self.payment.payment_status != "completed":
            raise ValidationError(
                "Review allowed only after completed payment"
            )

    def __str__(self):
        return f"{self.freelancer.username} - {self.rating}⭐"
