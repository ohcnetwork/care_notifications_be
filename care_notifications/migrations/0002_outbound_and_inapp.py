import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("care_notifications", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Notification",
            new_name="OutboundNotification",
        ),
        migrations.AlterField(
            model_name="outboundnotification",
            name="event_type",
            field=models.CharField(max_length=128),
        ),
        migrations.CreateModel(
            name="InAppNotification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("external_id", models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ("created_date", models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ("modified_date", models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ("deleted", models.BooleanField(db_index=True, default=False)),
                ("event_type", models.CharField(max_length=128)),
                ("resource_type", models.CharField(max_length=32)),
                ("resource_id", models.UUIDField()),
                ("title", models.CharField(max_length=255)),
                ("body", models.TextField(blank=True)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="in_app_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
