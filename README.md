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
| `BOOKING_CONFIRMATION_SMS_TEMPLATE` | `sms/booking_confirmation.txt` | Confirmation template path. |
| `BOOKING_REMINDER_SMS_TEMPLATE` | `sms/booking_reminder.txt` | Reminder template path. |
| `BOOKING_CANCEL_SMS_TEMPLATE` | `sms/booking_cancel.txt` | Cancel template path. |
| `BOOKING_RESCHEDULED_SMS_TEMPLATE` | `sms/booking_rescheduled.txt` | Reschedule template path. |


## Management commands

Backfill `BookingNotification` rows for active future `TokenBooking`s that pre-date this plug's install (without them, the sweep has nothing to drive off and those bookings will silently never get a reminder):

```bash
python manage.py backfill_booking_notifications
```
