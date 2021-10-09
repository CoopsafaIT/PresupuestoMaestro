# Generated by Django 3.0.10 on 2021-10-06 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_auto_20211004_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterParameters',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='FechaCreacion', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='FechaActualizacion', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('date_base', models.DateField(blank=True, db_column='FechaBase', null=True)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('comment', models.CharField(blank=True, db_column='Comentario', max_length=200, null=True)),
                ('name', models.CharField(blank=True, db_column='Nombre', max_length=50, null=True)),
                ('correlative', models.CharField(blank=True, db_column='Correlativo', max_length=50, null=True)),
                ('created_by', models.ForeignKey(db_column='CreadoPor', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('period_id', models.ForeignKey(db_column='PeriodoId', on_delete=django.db.models.deletion.DO_NOTHING, to='main.Periodo')),
                ('updated_by', models.ForeignKey(db_column='ActualizadoPor', on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_update', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pptoMaestroParametros',
                'ordering': ('name',),
                'default_permissions': [],
            },
        ),
    ]