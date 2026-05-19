from care.utils.models.base import BaseModel
from django.db import models

class BookingNotification(BaseModel):
    resource_type = models.CharField(max_length=32,)
    booking = models.ForeignKey(
        "emr.TokenBooking",
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    event_type = models.CharField(max_length=32,)
    sent_at = models.DateTimeField(auto_now_add=True)

