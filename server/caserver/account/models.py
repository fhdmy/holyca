from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class RepStats(models.Model):
    repstats_acc=models.CharField(max_length=100,default='')
    repstats_pwd=models.CharField(max_length=100,default='')
    repstats_id=models.IntegerField(default=0)
    auth=models.CharField(max_length=200,default='')
    
class Teammate(models.Model):
    nickname=models.CharField(max_length=100,default='新用户')
    score=models.IntegerField(default=0)
    has_signin=models.BooleanField(default=False)
    user = models.OneToOneField(
        to=User,
        # primary_key=True,
        on_delete=models.CASCADE,
        null=True
    )

    repstats=models.OneToOneField(
        to="RepStats",
        on_delete=models.CASCADE,
        null=True
    )
    
    def __str__(self):
        nickname = str(self.nickname)
        return nickname
