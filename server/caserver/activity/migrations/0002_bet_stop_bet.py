# Generated by Django 3.0.4 on 2020-05-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='stop_bet',
            field=models.BooleanField(default=False),
        ),
    ]
