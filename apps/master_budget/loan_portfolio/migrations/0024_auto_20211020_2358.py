# Generated by Django 3.0.10 on 2021-10-20 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_portfolio', '0023_auto_20211020_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialinvestments',
            name='rate',
            field=models.FloatField(blank=True, db_column='Tasa', default=0, null=True),
        ),
    ]
