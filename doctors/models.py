from django.db import models
from django.conf import settings


class Doctor(models.Model):

    # =========================================
    # SPECIALIZATION
    # =========================================

    SPECIALIZATION_CHOICES = (
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General Medicine'),
        ('gynecology', 'Gynecology'),
        ('ent', 'ENT'),
        ('dentistry', 'Dentistry'),
        ('psychiatry', 'Psychiatry'),
    )


    # =========================================
    # DOCTOR USER
    # =========================================

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )


    # =========================================
    # DOCTOR DETAILS
    # =========================================

    specialization = models.CharField(
        max_length=100,
        choices=SPECIALIZATION_CHOICES
    )

    qualification = models.CharField(
        max_length=200
    )

    experience = models.PositiveIntegerField(
        default=0
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    # =========================================
    # AVAILABILITY
    # =========================================

    available_days = models.CharField(
        max_length=200,
        blank=True
    )

    available_time = models.CharField(
        max_length=200,
        blank=True
    )

    is_available = models.BooleanField(
        default=True
    )


    # =========================================
    # DOCTOR BIO
    # =========================================

    bio = models.TextField(
        blank=True
    )


    # =========================================
    # CREATED DATE
    # =========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # =========================================
    # DISPLAY NAME
    # =========================================

    def __str__(self):

        full_name = self.user.get_full_name()

        if full_name:
            return f"Dr. {full_name}"

        return self.user.username