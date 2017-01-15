from django_cron import CronJobBase, Schedule
from Discover.views import post_message
from Discover.models import BotUser
from django.http import HttpResponse
import json



class MyCronJob(CronJobBase):
    RUN_EVERY_MINS =  1# 5every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Discover.MyCronJob' # a unique code

    def do(self):
        b_exists=BotUser.objects.all()
        for b in b_exists:
            post_message(b.user_id,"Hello")

            return HttpResponse(status=200)


