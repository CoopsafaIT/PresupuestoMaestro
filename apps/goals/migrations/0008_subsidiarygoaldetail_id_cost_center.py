# Generated by Django 3.0.10 on 2022-03-18 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20220308_2016'),
        ('goals', '0007_auto_20220316_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='subsidiarygoaldetail',
            name='id_cost_center',
            field=models.ForeignKey(db_column='IdFilial', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Centroscosto'),
        ),
    ]
