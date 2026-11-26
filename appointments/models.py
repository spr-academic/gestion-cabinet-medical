from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    # ? Design decision: Used PROTECT to preserve appointment history.
    doctor = models.ForeignKey(
        "cabinet.Doctor",
        on_delete=models.PROTECT
    )

    patient = models.ForeignKey(
        "cabinet.Patient",
        on_delete=models.PROTECT
    )

    reason = models.TextField()

    duration_minutes = models.PositiveIntegerField(default=30)

    scheduled_at = models.DateTimeField()

    # ? Design decision: Maximum status length is not specified.
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    # ? Project convention: Use "prescriptions/" instead of "ordonnances/".
    # ! FileExtensionValidator checks the extension, not the file content.
    prescription = models.FileField(
        upload_to="prescriptions/",
        blank=True,
        validators=[FileExtensionValidator(
            allowed_extensions=["pdf"]
        )]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "scheduled_at"],
                name="unique_doctor_appointment_time"
            )
        ]

    # ? Design decision: Provide a readable appointment representation.
    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.scheduled_at}"

    def clean(self):
        # NOTE: Call the inherited model validation method.
        super().clean()

        # Missing dates are handled by Django's field validation.
        if self.scheduled_at is None:
            return

        # Future appointments are valid.
        if self.scheduled_at > timezone.now():
            return

        # NOTE: _state.adding indicates whether the object is new.
        # Search for an existing appointment with the same primary key and scheduled date.
        if not self._state.adding and Appointment.objects.filter(
            pk=self.pk,
            scheduled_at=self.scheduled_at
        ).exists():
            return

        # ! Reject new or rescheduled appointments in the past.
        raise ValidationError({
            "scheduled_at": "Appointment must be in the future."
        })