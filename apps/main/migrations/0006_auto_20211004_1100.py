# Generated by Django 3.0.10 on 2021-10-04 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_detallexpresupuestoinversion_numero_meses_depreciacion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administracionpresupuesto',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='centrocostoxcuentacontable',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='centroscosto',
            options={'default_permissions': [], 'ordering': ('desccentrocosto',)},
        ),
        migrations.AlterModelOptions(
            name='criterios',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='cuentascontables',
            options={'default_permissions': [], 'ordering': ('desccuentacontable',)},
        ),
        migrations.AlterModelOptions(
            name='detallexpresupuestoinversion',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='detallexpresupuestopersonal',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='detallexpresupuestoviaticos',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='filiales',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='historicotraslados',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='historicotrasladosinversiones',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='historicotrasladosviaticos',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='inversiones',
            options={'default_permissions': [], 'ordering': ('descinversion',)},
        ),
        migrations.AlterModelOptions(
            name='manejodeviaticos',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='manejopersonal',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='periodo',
            options={'default_permissions': [], 'ordering': ('-descperiodo', '-fechalimite')},
        ),
        migrations.AlterModelOptions(
            name='presupuestocostos',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='presupuestoindirecto',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='presupuestoingresos',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='presupuestos',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='proyectos',
            options={'default_permissions': [], 'ordering': ('-fechainicio', 'descproyecto', 'codcentrocosto')},
        ),
        migrations.AlterModelOptions(
            name='puestos',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='responsablesporcentroscostos',
            options={'default_permissions': [], 'ordering': ('CodCentroCosto', 'CodUser', 'Estado')},
        ),
        migrations.AlterModelOptions(
            name='tipoaccionpresupuestoinversion',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='tipopresupuesto',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='tiposcuenta',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='transaccionesinversiones',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='transaccionesviaticos',
            options={'default_permissions': []},
        ),
        migrations.AlterModelOptions(
            name='valoresviativos',
            options={'default_permissions': []},
        ),
    ]
