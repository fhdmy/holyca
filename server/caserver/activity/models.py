from django.db import models
import django.utils.timezone as timezone
from datetime import datetime
import account.models

class Bet(models.Model):
    player_1=models.CharField(max_length=100,default='')
    player_2=models.CharField(max_length=100,default='')
    tournament=models.CharField(max_length=200,default='')
    match_url=models.CharField(max_length=300,default='')
    match_time=models.DateTimeField(default = timezone.now)
    finished=models.BooleanField(default=False)
    stop_bet=models.BooleanField(default=False)
    winner=models.CharField(max_length=100,default='')
    score=models.CharField(max_length=10,default='')

class Match(models.Model):
    tournament=models.CharField(max_length=200,default='')
    match_time=models.DateTimeField(default = timezone.now)

class Invest(models.Model):
    bet=models.ForeignKey(
        to=Bet,
        on_delete=models.CASCADE,
        related_name='invest',
        to_field="id",
        null=False
    )

    teammate=models.ForeignKey(
        to=account.models.Teammate,
        on_delete=models.CASCADE,
        related_name='invest',
        to_field="id",
        null=False
    )

    score=models.IntegerField(default=0)
    gain=models.IntegerField(default=0)
    target=models.CharField(max_length=100,default='')
    settled=models.BooleanField(default=False)  #是否被结算