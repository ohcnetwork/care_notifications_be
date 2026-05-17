from celery import Celery, current_app

from booking_notifications.settings import plugin_settings
from booking_notifications.tasks.notify_cancel import notify_cancel
from booking_notifications.tasks.notify_confirmation import notify_confirmation
from booking_notifications.tasks.notify_rescheduled import notify_rescheduled
from booking_notifications.tasks.send_reminder import send_reminder
from booking_notifications.tasks.sweep_reminders import sweep_reminders


@current_app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sweep = max(1, int(plugin_settings.BOOKING_REMINDER_SWEEP_MINUTES))
    sender.add_periodic_task(
        sweep * 60,
        sweep_reminders.s(),
        name="booking_notifications.sweep_reminders",
    )
