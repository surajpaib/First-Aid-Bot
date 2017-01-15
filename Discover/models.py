from __future__ import unicode_literals

from django.db import models

# Create your models here.


class BotUser(models.Model):
    user_id=models.CharField(max_length=20)
    user_card_count=models.IntegerField()




