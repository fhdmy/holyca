# Generated by Django 3.0.4 on 2020-05-07 07:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0009_auto_20200507_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mmr',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]