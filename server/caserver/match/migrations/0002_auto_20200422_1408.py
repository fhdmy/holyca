# Generated by Django 2.2 on 2020-04-22 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='battlenetaccount',
            name='basic_accomplishment',
            field=models.CharField(default='[]', max_length=200),
        ),
        migrations.AddField(
            model_name='battlenetaccount',
            name='map_winrate',
            field=models.CharField(default='[]', max_length=200),
        ),
        migrations.AddField(
            model_name='replay',
            name='kills',
            field=models.CharField(default='[]', max_length=200),
        ),
    ]