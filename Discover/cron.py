from django_cron import CronJobBase, Schedule
from Discover.views import main_card
from Discover.models import BotUser
from django.http import HttpResponse
import json



class MyCronJob(CronJobBase):
    RUN_EVERY_MINS =  1# 5every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Discover.MyCronJob' # a unique code

    def do(self):
        b_user=BotUser.objects.all()
        for b in b_user:
            with open('card_list.json','r') as fp:
                data=json.load(fp,'utf-8')
            main_card(b.user_id,data[b.user_card_count])

            b.user_card_count+=1
            b.save()

        return HttpResponse(status=200)


