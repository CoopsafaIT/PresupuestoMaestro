# Generated by Django 3.0.10 on 2021-10-12 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loan_portfolio', '0007_auto_20211011_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanPortfolioComment',
            fields=[
                ('comment', models.CharField(blank=True, db_column='Comentario', max_length=500, null=True)),
                ('deleted', models.BooleanField(blank=True, db_column='Borrado', default=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='FechaCreacion', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('created_by', models.ForeignKey(blank=True, db_column='CreadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('scenario_id', models.ForeignKey(blank=True, db_column='EscenarioId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='loan_portfolio.LoanPortfolioScenario')),
            ],
            options={
                'db_table': 'pptoMaestroCarteraCredMsj',
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='FinancialInvestmentsComment',
            fields=[
                ('comment', models.CharField(blank=True, db_column='Comentario', max_length=500, null=True)),
                ('deleted', models.BooleanField(blank=True, db_column='Borrado', default=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='FechaCreacion', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('created_by', models.ForeignKey(blank=True, db_column='CreadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('scenario_id', models.ForeignKey(blank=True, db_column='EscenarioId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='loan_portfolio.FinancialInvestmentsScenario')),
            ],
            options={
                'db_table': 'pptoMaestroInversionesFinMsj',
                'default_permissions': [],
            },
        ),
    ]
