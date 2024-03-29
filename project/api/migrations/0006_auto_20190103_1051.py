# Generated by Django 2.1.4 on 2019-01-03 10:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190103_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='date_from',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Product'),
        ),
        migrations.AlterField(
            model_name='price',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Shop'),
        ),
        migrations.DeleteModel(
            name='Product_tmp',
        ),
        migrations.DeleteModel(
            name='Shop_tmp',
        ),
    ]
