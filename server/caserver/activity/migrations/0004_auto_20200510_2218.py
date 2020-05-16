# Generated by Django 3.0.4 on 2020-05-10 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_repstats_last_submit'),
        ('activity', '0003_invest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invest',
            name='teammate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invest', to='account.Teammate'),
        ),
    ]