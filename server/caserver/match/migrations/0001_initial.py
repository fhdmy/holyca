# Generated by Django 3.0.4 on 2020-04-04 07:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BattlenetAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battlenet_name', models.CharField(default='', max_length=100)),
                ('battlenet_id', models.IntegerField(default=0, unique=True)),
                ('repstats_acc', models.ManyToManyField(related_name='battlenet_acc', to='account.RepStats')),
            ],
        ),
        migrations.CreateModel(
            name='Replay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rep_id', models.IntegerField(default=0)),
                ('player1_mmr', models.IntegerField(default=0)),
                ('player2_mmr', models.IntegerField(default=0)),
                ('winner', models.CharField(default='', max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('vs_race', models.CharField(default='', max_length=100)),
                ('game_length', models.CharField(default='', max_length=100)),
                ('game_map', models.CharField(default='', max_length=100)),
                ('player1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replay_player1', to='match.BattlenetAccount')),
                ('player2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replay_player2', to='match.BattlenetAccount')),
                ('repstats_acc', models.ManyToManyField(related_name='replay', to='account.RepStats')),
            ],
        ),
        migrations.CreateModel(
            name='MMR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mmr', models.IntegerField(default=0)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('battlenet_acc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mmr', to='match.BattlenetAccount')),
                ('replay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mmr', to='match.Replay')),
            ],
        ),
    ]
