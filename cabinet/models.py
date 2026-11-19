from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_birth_date(value):
    if value >= timezone.localdate():
        raise ValidationError("Birth date cannot be in the future.")

validate_eight_digit = RegexValidator(
        regex=r"\A[0-9]{8}\z",
        message="This field must be exactly 8 digits long."
    )

class User(AbstractUser):
    email = models.EmailField(unique=True)

class Patient(User):
    national_id = models.CharField(
        max_length=8,
        primary_key=True,
        validators=[validate_eight_digit]
    )

    phone_number = models.CharField(
        max_length=8,
        validators=[validate_eight_digit]
    )

    birth_date = models.DateField(validators=[validate_birth_date])
