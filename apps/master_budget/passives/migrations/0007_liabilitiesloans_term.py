# Generated by Django 3.0.10 on 2021-11-09 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passives', '0006_auto_20211109_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='liabilitiesloans',
            name='term',
            field=models.IntegerField(blank=True, db_column='Plazo', default=0, null=True),
        ),
    ]
