from enum import Enum


class NotificationType(str, Enum):
    confirmation = "confirmation"
    reminder = "reminder"
    cancellation = "cancellation"
    reschedule = "reschedule"
