# Generated by Django 3.0.10 on 2021-12-03 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_manejodeviaticos_categoria'),
        ('payment_payroll', '0003_auto_20211203_1101'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PaymentPayrollMonthlySalary',
            new_name='BasePaymentPayroll',
        ),
    ]
