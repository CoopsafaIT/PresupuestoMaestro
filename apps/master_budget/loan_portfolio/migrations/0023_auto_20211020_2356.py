# Generated by Django 3.0.10 on 2021-10-20 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_portfolio', '0022_auto_20211020_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialinvestments',
            name='amount_accounts_receivable',
            field=models.DecimalField(blank=True, db_column='MontoCuentasPorCobrar', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestments',
            name='amount_interest_earned',
            field=models.DecimalField(blank=True, db_column='MontoInteresGanado', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestments',
            name='new_amount',
            field=models.DecimalField(blank=True, db_column='MontoNuevo', decimal_places=2, default=0, max_digits=23, null=True),
        ),
    ]
