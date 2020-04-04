from django.db import models
import account.models
import django.utils.timezone as timezone

class BattlenetAccount(models.Model):
    battlenet_name=models.CharField(max_length=100,default='')
    battlenet_id=models.IntegerField(default=0,unique=True)

    repstats_acc=models.ManyToManyField(
        to=account.models.RepStats,
        related_name="battlenet_acc"
    )

class Replay(models.Model):
    rep_id=models.IntegerField(default=0)
    player1_mmr=models.IntegerField(default=0)
    player2_mmr=models.IntegerField(default=0)
    winner=models.CharField(max_length=100,default='')
    date=models.DateField(default = timezone.now)
    vs_race=models.CharField(max_length=100,default='')
    game_length=models.CharField(max_length=100,default='')
    game_map=models.CharField(max_length=100,default='')

    player1=models.ForeignKey(
        to=BattlenetAccount,
        on_delete=models.CASCADE,
        related_name='replay_player1',
        to_field="id",
        null=True
    )

    player2=models.ForeignKey(
        to=BattlenetAccount,
        on_delete=models.CASCADE,
        related_name='replay_player2',
        to_field="id",
        null=True
    )

    repstats_acc=models.ManyToManyField(
        to=account.models.RepStats,
        related_name="replay"
    )

class MMR(models.Model):
    mmr=models.IntegerField(default=0)
    date=models.DateField(default = timezone.now)
    
    replay=models.ForeignKey(
        to=Replay,
        on_delete=models.CASCADE,
        related_name='mmr',
        to_field="id",
        null=False
    )

    battlenet_acc=models.ForeignKey(
        to=BattlenetAccount,
        on_delete=models.CASCADE,
        related_name='mmr',
        to_field="id",
        null=False
    )