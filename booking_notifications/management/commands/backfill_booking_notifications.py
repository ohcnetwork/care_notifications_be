from django.core.management.base import BaseCommand
from django.utils import timezone

from booking_notifications.models.notification import BookingNotification
from care.emr.models.scheduling.booking import TokenBooking


class Command(BaseCommand):
    def handle(self, *args, **options):
        booking_ids = TokenBooking.objects.filter(
            status="booked",
            token_slot__start_datetime__gt=timezone.now(),
            notification_state__isnull=True,
        ).values_list("id", flat=True)

        rows = [BookingNotification(booking_id=bid) for bid in booking_ids]
        created = BookingNotification.objects.bulk_create(rows, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"Created {len(created)} BookingNotification row(s)."))
