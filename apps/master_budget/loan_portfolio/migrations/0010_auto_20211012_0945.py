# Generated by Django 3.0.10 on 2021-10-12 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loan_portfolio', '0009_auto_20211012_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialinvestmentscategory',
            name='created_by',
            field=models.ForeignKey(blank=True, db_column='CreadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='financialinvestmentscategory',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_column='ActualizadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_update_financial_investment_category', to=settings.AUTH_USER_MODEL),
        ),
    ]
