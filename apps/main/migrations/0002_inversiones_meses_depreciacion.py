# Generated by Django 3.0.10 on 2021-09-22 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inversiones',
            name='meses_depreciacion',
            field=models.IntegerField(blank=True, db_column='MesesDepreciacion', null=True),
        ),
    ]
