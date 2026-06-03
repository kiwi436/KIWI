from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiwi', '0005_clase_usuario_ideakleit_usuario_plandeaula_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesionkleit',
            name='titulo_sesion',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='sesionkleit',
            name='mensajes',
            field=models.TextField(blank=True, default='[]'),
        ),
        migrations.AddField(
            model_name='sesionkleit',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='sesionkleit',
            name='tema',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='sesionkleit',
            name='grupo',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterModelOptions(
            name='sesionkleit',
            options={'ordering': ['-updated_at']},
        ),
    ]
