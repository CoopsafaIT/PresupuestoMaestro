# Generated by Django 3.0.10 on 2021-10-25 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_portfolio', '0025_auto_20211025_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_april',
            field=models.DecimalField(blank=True, db_column='DisminucionesAbr', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_august',
            field=models.DecimalField(blank=True, db_column='DisminucionesAgo', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_december',
            field=models.DecimalField(blank=True, db_column='DisminucionesDic', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_february',
            field=models.DecimalField(blank=True, db_column='DisminucionesFeb', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_january',
            field=models.DecimalField(blank=True, db_column='DisminucionesEne', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_july',
            field=models.DecimalField(blank=True, db_column='DisminucionesJul', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_june',
            field=models.DecimalField(blank=True, db_column='DisminucionesJun', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_march',
            field=models.DecimalField(blank=True, db_column='DisminucionesMar', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_may',
            field=models.DecimalField(blank=True, db_column='DisminucionesMay', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_november',
            field=models.DecimalField(blank=True, db_column='DisminucionesNov', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_october',
            field=models.DecimalField(blank=True, db_column='DisminucionesOct', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='decreases_september',
            field=models.DecimalField(blank=True, db_column='DisminucionesSep', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_april',
            field=models.DecimalField(blank=True, db_column='AumentoAbr', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_august',
            field=models.DecimalField(blank=True, db_column='AumentoAgo', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_december',
            field=models.DecimalField(blank=True, db_column='AumentoDic', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_february',
            field=models.DecimalField(blank=True, db_column='AumentoFeb', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_january',
            field=models.DecimalField(blank=True, db_column='AumentoEne', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_july',
            field=models.DecimalField(blank=True, db_column='AumentoJul', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_june',
            field=models.DecimalField(blank=True, db_column='AumentoJun', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_march',
            field=models.DecimalField(blank=True, db_column='AumentoMar', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_may',
            field=models.DecimalField(blank=True, db_column='AumentoMay', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_november',
            field=models.DecimalField(blank=True, db_column='AumentoNov', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_october',
            field=models.DecimalField(blank=True, db_column='AumentoOct', decimal_places=2, default=0, max_digits=23, null=True),
        ),
        migrations.AlterField(
            model_name='financialinvestmentsscenario',
            name='increases_september',
            field=models.DecimalField(blank=True, db_column='AumentoSep', decimal_places=2, default=0, max_digits=23, null=True),
        ),
    ]
