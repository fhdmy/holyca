# Generated by Django 3.0.4 on 2020-05-07 05:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_mmr_race'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mmr',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='replay',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
