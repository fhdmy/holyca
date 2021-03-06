# Generated by Django 3.0.4 on 2020-05-10 12:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_1', models.CharField(default='', max_length=100)),
                ('player_2', models.CharField(default='', max_length=100)),
                ('tournament', models.CharField(default='', max_length=200)),
                ('match_url', models.CharField(default='', max_length=300)),
                ('match_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('finished', models.BooleanField(default=False)),
                ('winner', models.CharField(default='', max_length=100)),
                ('score', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament', models.CharField(default='', max_length=200)),
                ('match_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
