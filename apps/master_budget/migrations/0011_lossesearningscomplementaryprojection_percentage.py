# Generated by Django 3.0.10 on 2022-03-02 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_budget', '0010_surplusdistribution_surplusdistributioncategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='lossesearningscomplementaryprojection',
            name='percentage',
            field=models.FloatField(blank=True, db_column='Porcentaje', default=0, null=True),
        ),
    ]