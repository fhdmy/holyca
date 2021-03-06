# Generated by Django 3.0.4 on 2020-05-10 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_repstats_last_submit'),
        ('activity', '0002_bet_stop_bet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('target', models.CharField(default='', max_length=100)),
                ('settled', models.BooleanField(default=False)),
                ('bet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invest', to='activity.Bet')),
                ('teammate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invest', to='account.Teammate', to_field='user')),
            ],
        ),
    ]
