from care.utils.models.base import BaseModel
from django.db import models


class BookingNotification(BaseModel):
    booking = models.OneToOneField(
        "emr.TokenBooking",
        on_delete=models.CASCADE,
        related_name="notification_state",
    )
    confirmation_sent_at = models.DateTimeField(null=True, blank=True)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)
    cancel_sent_at = models.DateTimeField(null=True, blank=True)
    rescheduled_sent_at = models.DateTimeField(null=True, blank=True)
