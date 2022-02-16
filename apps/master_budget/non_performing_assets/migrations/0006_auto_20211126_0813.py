# Generated by Django 3.0.10 on 2021-11-26 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('non_performing_assets', '0005_otherassets_otherassetscategory_otherassetsscenario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherassetsscenario',
            name='category_id',
        ),
        migrations.AddField(
            model_name='otherassets',
            name='category_id',
            field=models.ForeignKey(blank=True, db_column='CategoryId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='non_performing_assets.OtherAssetsCategory'),
        ),
    ]
