# Generated by Django 3.0.10 on 2021-12-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_payroll', '0007_auto_20211205_0748'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentpayroll',
            name='permanent_staff_number',
            field=models.IntegerField(blank=True, db_column='CantidadEmpleadosPermanentes', default=0, null=True),
        ),
        migrations.AddField(
            model_name='paymentpayroll',
            name='temp_staff_number',
            field=models.IntegerField(blank=True, db_column='CantidadEmpleadosTemporales', default=0, null=True),
        ),
    ]
