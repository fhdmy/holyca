from django.db import models
from django.contrib.auth.models import User

class Teammate(models.Model):
    nickname=models.CharField(max_length=100,default='新用户')
    score=models.IntegerField(default=0)
    auth=models.CharField(max_length=200,default='')
    has_signin=models.BooleanField(default=False)
    repstats_acc=models.CharField(max_length=100,default='holyca@126.com')
    repstats_pwd=models.CharField(max_length=100,default='')
    user = models.OneToOneField(
        to=User,
        # primary_key=True,
        on_delete=models.CASCADE,
        null=True
    )
    
    def __str__(self):
        nickname = str(self.nickname)
        return nickname