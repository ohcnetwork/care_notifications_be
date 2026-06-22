from enum import Enum


class ResourceType(str, Enum):
    booking = "booking"
    diagnostic_report = "diagnostic_report"
    service_request = "service_request"
    encounter = "encounter"
    medication_stock = "medication_stock"


class EventType(str, Enum):
    booking_confirmation = "booking_confirmation"
    booking_reminder = "booking_reminder"
    booking_cancellation = "booking_cancellation"
    booking_reschedule = "booking_reschedule"
    diagnostic_report_ready = "diagnostic_report_ready"
    service_request_raised = "service_request_raised"
    encounter_ip_created = "encounter_ip_created"
    medication_stock_near_expiry = "medication_stock_near_expiry"
    medication_stock_low = "medication_stock_low"

