# Generated by Django 3.0.4 on 2020-05-07 07:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0005_auto_20200507_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mmr',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 7, 15, 2, 55, 742938)),
        ),
        migrations.AlterField(
            model_name='replay',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 7, 15, 2, 55, 739912)),
        ),
    ]