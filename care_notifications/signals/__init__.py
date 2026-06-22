# Importing the receiver module connects the signal handlers at app ready().
from care_notifications.signals import (  # noqa: F401
    booking,
    diagnostic_report,
    encounter,
    service_request,
)
