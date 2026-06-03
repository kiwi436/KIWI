from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiwi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clase',
            name='google_event_id',
            field=models.CharField(
                blank=True, max_length=200,
                help_text='ID del evento en Google Calendar'
            ),
        ),
    ]
