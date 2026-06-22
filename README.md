# care_notifications_be

CARE plug that sends notifications to patients (SMS) and clinicians (in-app).

## Currently supports

1. Token bookings — confirm, reminder, cancel, reschedule. (SMS)
2. Service requests — raised. (in-app)
3. Diagnostic reports — ready. (in-app)
4. Encounters — IP admission with location assigned. (in-app)
5. Medication stock — near expiry, low stock. (in-app)

## Install

Add to `plug_config.py`:

```python
care_notifications = Plug(
    name="care_notifications",
    package_name="git+https://github.com/ohcnetwork/care_notifications_be.git@main",
    version="0.1.0",
    configs={},
)
plugs = [care_notifications]
```

Then `make build && make up`.

## Settings

### Token bookings (SMS)

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

### Service requests (in-app)

| Key | Default | Description |
|---|---|---|
| `SERVICE_REQUEST_NOTIFICATIONS_ENABLED` | `True` | Master switch for all service request notifications. |
| `SERVICE_REQUEST_NOTIFY_RAISED` | `True` | Notify when an SR transitions to `active`. Sent to members of `sr.healthcare_service.managing_organization`. |
| `SERVICE_REQUEST_RAISED_TITLE` | `New {service_request_title} request` | Inbox title. |
| `SERVICE_REQUEST_RAISED_BODY` | `Patient: {patient_name}` | Inbox body. |

### Diagnostic reports (in-app)

| Key | Default | Description |
|---|---|---|
| `DIAGNOSTIC_REPORT_NOTIFICATIONS_ENABLED` | `True` | Master switch for all diagnostic report notifications. |
| `DIAGNOSTIC_REPORT_NOTIFY_READY` | `True` | Notify when a DR transitions to `final`. Sent to the originating SR's requester. |
| `DIAGNOSTIC_REPORT_READY_TITLE` | `Diagnostic report ready for {patient_name}` | Inbox title. |
| `DIAGNOSTIC_REPORT_READY_BODY` | `` | Inbox body (empty by default; title carries enough). |

### Encounters (in-app)

| Key | Default | Description |
|---|---|---|
| `ENCOUNTER_NOTIFICATIONS_ENABLED` | `True` | Master switch for all encounter notifications. |
| `ENCOUNTER_NOTIFY_IP_CREATED` | `True` | Notify when an encounter newly becomes IP (`encounter_class="imp"`) with a `current_location` assigned. Sent to care team + members of every facility-org in the encounter's access cache. |
| `ENCOUNTER_IP_CREATED_TITLE` | `New IP encounter: {patient_name}` | Inbox title. |
| `ENCOUNTER_IP_CREATED_BODY` | `Location: {location_name}` | Inbox body. |

### Medication stock (in-app)

| Key | Default | Description |
|---|---|---|
| `MEDICATION_NOTIFICATIONS_ENABLED` | `True` | Master switch for all medication stock notifications. |
| `MEDICATION_NOTIFY_NEAR_EXPIRY` | `True` | Notify when a medication InventoryItem's product expires within the lead window and has stock on hand. |
| `MEDICATION_NOTIFY_LOW_STOCK` | `True` | Notify when a medication InventoryItem's `net_content` drops below the threshold. |
| `MEDICATION_STOCK_SWEEP_MINUTES` | `1440` | How often the medication stock sweep runs. |
| `MEDICATION_NEAR_EXPIRY_LEAD_DAYS` | `30` | Days before expiry at which to fire near-expiry. |
| `MEDICATION_LOW_STOCK_THRESHOLD` | `10` | Threshold below which `net_content` triggers low-stock. |
| `MEDICATION_NEAR_EXPIRY_TITLE` | `Medication near expiry: {product_name}` | Inbox title. |
| `MEDICATION_NEAR_EXPIRY_BODY` | `Expires {expiration_date}. Location: {location_name}.` | Inbox body. |
| `MEDICATION_LOW_STOCK_TITLE` | `Low stock: {product_name}` | Inbox title. |
| `MEDICATION_LOW_STOCK_BODY` | `Remaining {net_content}. Location: {location_name}.` | Inbox body. |

Message bodies are Python `str.format` templates. Available placeholders per event:

| Event | Placeholders |
|---|---|
| Booking (all 4) | `{patient_name}`, `{slot_start}` (timezone-aware datetime; supports format specs like `{slot_start:%d %b %H:%M}`) |
| Service request raised | `{patient_name}`, `{service_request_title}` |
| Diagnostic report ready | `{patient_name}` |
| Encounter IP created | `{patient_name}`, `{location_name}` |
| Medication near expiry | `{product_name}`, `{expiration_date}`, `{location_name}`, `{net_content}` |
| Medication low stock | `{product_name}`, `{net_content}`, `{location_name}` |

## API

The plug exposes two read-only endpoints under `/api/care_notifications/`:

| Path | Purpose |
|---|---|
| `GET /in_app_notifications/` | Inbox feed. Returns the caller's own rows; superuser sees all. Filter by `event_type`, `resource_type`, `resource_id`. |
| `GET /outbound_notifications/` | SMS audit log. Filter by the same params. |
