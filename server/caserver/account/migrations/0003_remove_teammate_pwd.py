# Generated by Django 2.2 on 2020-03-25 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200324_2301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammate',
            name='pwd',
        ),
    ]
