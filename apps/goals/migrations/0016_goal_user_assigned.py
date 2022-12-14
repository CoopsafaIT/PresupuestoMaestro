# Generated by Django 3.0.10 on 2022-04-04 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0015_auto_20220329_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='user_assigned',
            field=models.ForeignKey(
                blank=True,
                db_column='UsuarioAsignado',
                null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='asignado',
                to=settings.AUTH_USER_MODEL),
        ),
    ]
