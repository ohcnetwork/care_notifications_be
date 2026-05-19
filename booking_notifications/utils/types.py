from enum import Enum


class ResourceType(str, Enum):
    booking = "booking"


class EventType(str, Enum):
    confirmation = "confirmation"
    reminder = "reminder"
    cancellation = "cancellation"
    reschedule = "reschedule"

