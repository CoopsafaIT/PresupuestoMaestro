# Generated by Django 3.0.10 on 2021-10-09 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loan_portfolio', '0005_auto_20211009_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanportfolio',
            name='created_by',
            field=models.ForeignKey(blank=True, db_column='CreadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loanportfolio',
            name='scenario_id',
            field=models.ForeignKey(blank=True, db_column='EscenarioId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='loan_portfolio.LoanPortfolioScenario'),
        ),
        migrations.AlterField(
            model_name='loanportfolio',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_column='ActualizadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_upd_loan_portfolio', to=settings.AUTH_USER_MODEL),
        ),
    ]
