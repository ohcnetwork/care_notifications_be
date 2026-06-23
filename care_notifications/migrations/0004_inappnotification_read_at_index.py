from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("care_notifications", "0003_rename_booking_not_resourc_b8e6a4_idx_care_notifi_resourc_9b251a_idx"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inappnotification",
            name="read_at",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
