# care_booking_notifications_be

Plug for CARE that sends SMS notifications to patients on booking confirm, reminder, cancel, and reschedule.

## Settings

| Key | Default | Description |
|---|---|---|
| `BOOKING_REMINDER_LEAD_MINUTES` | `60` | Minutes before slot start to send the reminder. |
| `BOOKING_REMINDER_SWEEP_MINUTES` | `1` | How often the reminder sweep runs. |
| `BOOKING_NOTIFY_SMS_ENABLED` | `True` | Master switch for SMS dispatch. |
| `BOOKING_NOTIFY_CONFIRMATION` | `True` | Send confirmation SMS. |
| `BOOKING_NOTIFY_REMINDER` | `True` | Send reminder SMS. |
| `BOOKING_NOTIFY_CANCEL` | `True` | Send cancellation SMS. |
| `BOOKING_NOTIFY_RESCHEDULED` | `True` | Send reschedule SMS. |
| `BOOKING_NOTIFY_SMS_SENDER` | `""` | Overrides `DEFAULT_SMS_SENDER` for these messages. |
| `BOOKING_CONFIRMATION_SMS_TEXT` | `Hi {patient_name}, your appointment is confirmed for {slot_start:%a, %d %b %Y %H:%M}. - Care` | Confirmation SMS body. |
| `BOOKING_REMINDER_SMS_TEXT` | `Reminder: {patient_name}, your appointment is at {slot_start:%a, %d %b %Y %H:%M}. - Care` | Reminder SMS body. |
| `BOOKING_CANCEL_SMS_TEXT` | `Hi {patient_name}, your appointment for {slot_start:%a, %d %b %Y %H:%M} has been cancelled. - Care` | Cancel SMS body. |
| `BOOKING_RESCHEDULED_SMS_TEXT` | `Hi {patient_name}, your previous appointment has been rescheduled. - Care` | Reschedule SMS body. |

Message bodies are Python `str.format` templates. Available placeholders: `{patient_name}`, `{slot_start}` (a timezone-aware datetime; supports format specs like `{slot_start:%d %b %H:%M}`).
