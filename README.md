# care_booking_notifications_be

CARE plug that sends notifications to patients.

## Currently supports

1. Token bookings — confirm, reminder, cancel, reschedule.

## Install

Add to `plug_config.py`:

```python
booking_notifications = Plug(
    name="booking_notifications",
    package_name="git+https://github.com/ohcnetwork/care_notifications_be.git@main",
    version="0.1.0",
    configs={},
)
plugs = [booking_notifications]
```

Then `make build && make up`.

## Settings

| Key | Default | Description |
|---|---|---|
| `TOKEN_BOOKING_NOTIFICATIONS_ENABLED` | `True` | Master switch for all token booking notifications. |
| `BOOKING_REMINDER_LEAD_MINUTES` | `60` | Minutes before slot start to send the reminder. |
| `BOOKING_REMINDER_SWEEP_MINUTES` | `1` | How often the reminder sweep runs. |
| `BOOKING_NOTIFY_CONFIRMATION` | `True` | Send confirmation SMS. |
| `BOOKING_NOTIFY_REMINDER` | `True` | Send reminder SMS. |
| `BOOKING_NOTIFY_CANCEL` | `True` | Send cancellation SMS. |
| `BOOKING_NOTIFY_RESCHEDULED` | `True` | Send reschedule SMS. |
| `BOOKING_CONFIRMATION_SMS_TEXT` | `Hi {patient_name}, your appointment is confirmed for {slot_start:%a, %d %b %Y %H:%M}. - Care` | Confirmation SMS body. |
| `BOOKING_REMINDER_SMS_TEXT` | `Reminder: {patient_name}, your appointment is at {slot_start:%a, %d %b %Y %H:%M}. - Care` | Reminder SMS body. |
| `BOOKING_CANCEL_SMS_TEXT` | `Hi {patient_name}, your appointment for {slot_start:%a, %d %b %Y %H:%M} has been cancelled. - Care` | Cancel SMS body. |
| `BOOKING_RESCHEDULED_SMS_TEXT` | `Hi {patient_name}, your previous appointment has been rescheduled. - Care` | Reschedule SMS body. |

Message bodies are Python `str.format` templates. Available placeholders: `{patient_name}`, `{slot_start}` (a timezone-aware datetime; supports format specs like `{slot_start:%d %b %H:%M}`).
