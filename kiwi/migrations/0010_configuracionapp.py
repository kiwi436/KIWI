from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiwi', '0009_usuario_email_verificado_google_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmail_refresh_token', models.CharField(blank=True, max_length=500)),
                ('gmail_email', models.EmailField(blank=True, max_length=254)),
            ],
            options={
                'verbose_name': 'Configuración',
            },
        ),
    ]
