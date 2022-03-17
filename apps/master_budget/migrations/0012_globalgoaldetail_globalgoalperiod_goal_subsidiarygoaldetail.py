# Generated by Django 3.0.10 on 2022-03-04 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0007_manejodeviaticos_categoria'),
        ('master_budget', '0011_lossesearningscomplementaryprojection_percentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalGoalPeriod',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='FechaCreacion', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='FechaActualizacion', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, db_column='Descripcion', max_length=500, null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='CreadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('period_id', models.ForeignKey(blank=True, db_column='PeriodoId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Periodo')),
                ('updated_by', models.ForeignKey(blank=True, db_column='ActualizadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_update_global_goal_period', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MetasGlobalPeriodo',
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='SubsidiaryGoalDetail',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='FechaCreacion', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='FechaActualizacion', null=True)),
                ('amount_january', models.DecimalField(blank=True, db_column='MontoEne', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_february', models.DecimalField(blank=True, db_column='MontoFeb', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_march', models.DecimalField(blank=True, db_column='MontoMar', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_april', models.DecimalField(blank=True, db_column='MontoAbr', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_may', models.DecimalField(blank=True, db_column='MontoMay', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_june', models.DecimalField(blank=True, db_column='MontoJun', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_july', models.DecimalField(blank=True, db_column='MontoJul', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_august', models.DecimalField(blank=True, db_column='MontoAgo', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_september', models.DecimalField(blank=True, db_column='MontoSep', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_october', models.DecimalField(blank=True, db_column='MontoOct', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_november', models.DecimalField(blank=True, db_column='MontoNov', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_december', models.DecimalField(blank=True, db_column='MontoDic', decimal_places=2, default=0, max_digits=23, null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('annual_amount_subsidiary', models.DecimalField(blank=True, db_column='MontoAnualFilial', decimal_places=2, default=0, max_digits=23, null=True)),
                ('ponderation', models.FloatField(blank=True, db_column='Ponderacion', default=0, null=True)),
                ('percentage', models.FloatField(blank=True, db_column='Porcentaje', default=0, null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='CreadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('id_global_goal_period', models.ForeignKey(db_column='IdMetasGlobalesPeriodo', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='master_budget.GlobalGoalPeriod')),
                ('updated_by', models.ForeignKey(blank=True, db_column='ActualizadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_update_subsidiary_goal_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MetasFilialDetalle',
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='FechaCreacion', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='FechaActualizacion', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, db_column='Descripcion', max_length=500, null=True)),
                ('type', models.CharField(blank=True, choices=[('I', 'Ingresos'), ('P', 'Perdidas')], db_column='Tipo', max_length=1, null=True)),
                ('manual_definition', models.CharField(blank=True, db_column='DefinicionManual', max_length=200, null=True)),
                ('manual_execution', models.CharField(blank=True, db_column='EjecucionManual', max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='CreadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_column='ActualizadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_update_goal', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Metas',
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='GlobalGoalDetail',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='FechaCreacion', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='FechaActualizacion', null=True)),
                ('amount_january', models.DecimalField(blank=True, db_column='MontoEne', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_february', models.DecimalField(blank=True, db_column='MontoFeb', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_march', models.DecimalField(blank=True, db_column='MontoMar', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_april', models.DecimalField(blank=True, db_column='MontoAbr', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_may', models.DecimalField(blank=True, db_column='MontoMay', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_june', models.DecimalField(blank=True, db_column='MontoJun', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_july', models.DecimalField(blank=True, db_column='MontoJul', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_august', models.DecimalField(blank=True, db_column='MontoAgo', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_september', models.DecimalField(blank=True, db_column='MontoSep', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_october', models.DecimalField(blank=True, db_column='MontoOct', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_november', models.DecimalField(blank=True, db_column='MontoNov', decimal_places=2, default=0, max_digits=23, null=True)),
                ('amount_december', models.DecimalField(blank=True, db_column='MontoDic', decimal_places=2, default=0, max_digits=23, null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('annual_amount', models.DecimalField(blank=True, db_column='MontoAnual', decimal_places=2, default=0, max_digits=23, null=True)),
                ('ponderation', models.FloatField(blank=True, db_column='Ponderacion', default=0, null=True)),
                ('percentage', models.FloatField(blank=True, db_column='Porcentaje', default=0, null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='CreadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('id_global_goal_period', models.ForeignKey(db_column='IdMetasGlobalesPeriodo', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='master_budget.GlobalGoalPeriod')),
                ('id_goal', models.ForeignKey(db_column='IdMetas', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='master_budget.Goal')),
                ('updated_by', models.ForeignKey(blank=True, db_column='ActualizadoPor', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_update_global_goal_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MetaGlobalDetalle',
                'default_permissions': [],
            },
        ),
    ]