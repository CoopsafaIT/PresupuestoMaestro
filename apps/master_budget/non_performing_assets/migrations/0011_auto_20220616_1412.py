# Generated by Django 3.0.10 on 2022-06-16 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('non_performing_assets', '0010_auto_20220616_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_april',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_august',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_december',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_february',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_january',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_july',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_june',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_march',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_may',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_november',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_october',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='amount_september',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_april',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_august',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_december',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_february',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_january',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_july',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_june',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_march',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_may',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_november',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_october',
        ),
        migrations.RemoveField(
            model_name='nonperformingassetsxcategory',
            name='percentage_september',
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_april',
            field=models.DecimalField(blank=True, db_column='MontoAbr', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_august',
            field=models.DecimalField(blank=True, db_column='MontoAgo', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_december',
            field=models.DecimalField(blank=True, db_column='MontoDic', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_february',
            field=models.DecimalField(blank=True, db_column='MontoFeb', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_january',
            field=models.DecimalField(blank=True, db_column='MontoEne', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_july',
            field=models.DecimalField(blank=True, db_column='MontoJul', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_june',
            field=models.DecimalField(blank=True, db_column='MontoJun', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_march',
            field=models.DecimalField(blank=True, db_column='MontoMar', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_may',
            field=models.DecimalField(blank=True, db_column='MontoMay', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_november',
            field=models.DecimalField(blank=True, db_column='MontoNov', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_october',
            field=models.DecimalField(blank=True, db_column='MontoOct', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='amount_september',
            field=models.DecimalField(blank=True, db_column='MontoSep', decimal_places=4, default=0, max_digits=23, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_april',
            field=models.FloatField(blank=True, db_column='PorcentajeAbr', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_august',
            field=models.FloatField(blank=True, db_column='PorcentajeAgo', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_december',
            field=models.FloatField(blank=True, db_column='PorcentajeDic', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_february',
            field=models.FloatField(blank=True, db_column='PorcentajeFeb', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_january',
            field=models.FloatField(blank=True, db_column='PorcentajeEne', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_july',
            field=models.FloatField(blank=True, db_column='PorcentajeJul', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_june',
            field=models.FloatField(blank=True, db_column='PorcentajeJun', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_march',
            field=models.FloatField(blank=True, db_column='PorcentajeMar', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_may',
            field=models.FloatField(blank=True, db_column='PorcentajeMay', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_november',
            field=models.FloatField(blank=True, db_column='PorcentajeNov', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_october',
            field=models.FloatField(blank=True, db_column='PorcentajeOct', default=0, null=True),
        ),
        migrations.AddField(
            model_name='otherassets',
            name='percentage_september',
            field=models.FloatField(blank=True, db_column='PorcentajeSep', default=0, null=True),
        ),
    ]
