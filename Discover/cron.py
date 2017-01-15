from django_cron import CronJobBase, Schedule
from Discover.views import cron_main_card,post_message
from Discover.models import BotUser
from django.http import HttpResponse
import json



class MyCronJob(CronJobBase):
    RUN_EVERY_MINS =  1# 5every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Discover.MyCronJob' # a unique code

    def do(self):
        b_user = BotUser.objects.all()
        for b in b_user:

            with open('card_list.json', 'r') as fp:
                data = json.load(fp, 'utf-8')
            post_message(b.user_id,"Hello there!! Here's todays discovery!")
            cron_main_card(b.user_id, data[b.user_card_count],b)

            return HttpResponse(status=200)


