# Generated by Django 3.0.10 on 2021-10-06 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_auto_20211004_1100'),
        ('master_budget', '0002_auto_20211006_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterparameters',
            name='updated_by',
            field=models.ForeignKey(db_column='ActualizadoPor', on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_update_parameter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='LoanPortfolioCategory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='FechaCreacion', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='FechaActualizacion', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Nombre', max_length=50, null=True)),
                ('is_active', models.BooleanField(blank=True, db_column='Estado', default=True, null=True)),
                ('identifier', models.CharField(blank=True, db_column='Identificador', max_length=50, null=True)),
                ('created_by', models.ForeignKey(db_column='CreadoPor', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(db_column='ActualizadoPor', on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_update_loan_portfolio_category', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pptoMaestroCartCredCategoria',
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='LoanPortfolio',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='FechaCreacion', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='FechaActualizacion', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('month', models.CharField(blank=True, choices=[('', '-- Seleccione Mes --'), (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')], db_column='Mes', max_length=50, null=True)),
                ('amount_initial', models.DecimalField(blank=True, db_column='MontoInicial', decimal_places=2, max_digits=23, null=True)),
                ('percent_growth', models.FloatField(blank=True, db_column='PorcentajeCrecimiento', null=True)),
                ('amount_growth', models.DecimalField(blank=True, db_column='MontoCrecimiento', decimal_places=2, max_digits=23, null=True)),
                ('new_amount', models.DecimalField(blank=True, db_column='MontoNuevo', decimal_places=2, max_digits=23, null=True)),
                ('rate', models.FloatField(blank=True, db_column='Tasa', null=True)),
                ('term', models.IntegerField(blank=True, db_column='Plazo', null=True)),
                ('level_quota', models.DecimalField(blank=True, db_column='CuotaNivelada', decimal_places=2, max_digits=23, null=True)),
                ('total_interest', models.DecimalField(blank=True, db_column='InteresesTotales', decimal_places=2, max_digits=23, null=True)),
                ('principal_payments', models.DecimalField(blank=True, db_column='PagosCapital', decimal_places=2, max_digits=23, null=True)),
                ('percentage_arrears', models.FloatField(blank=True, db_column='PorcentajeMora', null=True)),
                ('amount_arrears', models.DecimalField(blank=True, db_column='MontoMora', decimal_places=2, max_digits=23, null=True)),
                ('default_interest', models.DecimalField(blank=True, db_column='InteresesMoratorios', decimal_places=2, max_digits=23, null=True)),
                ('commission_percentage', models.FloatField(blank=True, db_column='PorcentajeComision', null=True)),
                ('commission_amount', models.DecimalField(blank=True, db_column='MontoComision', decimal_places=2, max_digits=23, null=True)),
                ('correlative', models.CharField(blank=True, db_column='Correlativo', max_length=50, null=True)),
                ('comment', models.CharField(blank=True, db_column='Comentario', max_length=500, null=True)),
                ('is_active', models.BooleanField(blank=True, db_column='Estado', default=True, null=True)),
                ('category_id', models.ForeignKey(db_column='CategoriaId', on_delete=django.db.models.deletion.DO_NOTHING, to='master_budget.LoanPortfolioCategory')),
                ('created_by', models.ForeignKey(db_column='CreadoPor', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('parameter_id', models.ForeignKey(db_column='ParametroId', on_delete=django.db.models.deletion.DO_NOTHING, to='master_budget.MasterParameters')),
                ('period_id', models.ForeignKey(db_column='PeriodoId', on_delete=django.db.models.deletion.DO_NOTHING, to='main.Periodo')),
                ('updated_by', models.ForeignKey(db_column='ActualizadoPor', on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_upd_loan_portfolio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pptoMaestroCartCred',
                'default_permissions': [],
            },
        ),
    ]
