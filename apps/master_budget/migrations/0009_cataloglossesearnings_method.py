# Generated by Django 3.0.10 on 2021-12-14 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_budget', '0008_auto_20211214_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='cataloglossesearnings',
            name='method',
            field=models.CharField(blank=True, db_column='Metodo', max_length=1, null=True),
        ),
    ]
