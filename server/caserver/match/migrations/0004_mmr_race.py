# Generated by Django 3.0.4 on 2020-05-07 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0003_auto_20200422_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmr',
            name='race',
            field=models.CharField(default='', max_length=10),
        ),
    ]