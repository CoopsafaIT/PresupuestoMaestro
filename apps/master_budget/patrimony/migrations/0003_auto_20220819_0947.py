# Generated by Django 3.0.10 on 2022-08-19 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20220308_2016'),
        ('patrimony', '0002_distribution_surplus_period_distributionsurplus_category_surplus_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DistributionSurplus_category',
            new_name='DistributionSurplusCategory',
        ),
        migrations.RenameModel(
            old_name='Distribution_surplus_period',
            new_name='DistributionSurplusPeriod',
        ),
        migrations.RenameModel(
            old_name='Surplus_category',
            new_name='SurplusCategory',
        ),
    ]
