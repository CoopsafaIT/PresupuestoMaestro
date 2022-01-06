# Generated by Django 3.0.10 on 2021-11-21 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_manejodeviaticos_categoria'),
        ('non_performing_assets', '0002_auto_20211120_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonPerformingAssetsCategoryMapAccounts',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('account_id', models.ForeignKey(blank=True, db_column='CuentaContableId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Cuentascontables')),
                ('category_id', models.ForeignKey(blank=True, db_column='CategoriaId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='non_performing_assets.NonPerformingAssetsCategory')),
            ],
            options={
                'db_table': 'pptoMaestroActivosFijosCatXCuentasContables',
                'default_permissions': [],
            },
        ),
    ]
