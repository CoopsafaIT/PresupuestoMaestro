# Generated by Django 3.0.10 on 2021-10-20 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_portfolio', '0017_loanportfolioscenario_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanportfolioscenario',
            name='deleted',
            field=models.BooleanField(blank=True, db_column='Eliminado', default=False, null=True),
        ),
    ]
