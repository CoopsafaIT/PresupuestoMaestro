# Generated by Django 3.0.10 on 2021-12-13 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_id', models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user_validate_ad', models.BooleanField(blank=True, db_column='ValidarConAD', default=False, null=True)),
            ],
            options={
                'db_table': 'auth_user_profile',
            },
        ),
    ]
