from django_cron import CronJobBase, Schedule
from AidBot.views import cron_main_card,post_message
from AidBot.models import BotUser
from django.http import HttpResponse
import json


urls = [{'url': 'https://2.sendvid.com/ob29ioyt.mp4', 'text': 'Asthma'},
        {'url': 'https://2.sendvid.com/a0xjqwuq.mp4', 'text': 'Heavy Bleeding'}]
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # 5every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'AidBot.MyCronJob' # a unique code



    def do(self):
        b_user = BotUser.objects.all()
        for b in b_user:

            post_message(b.user_id, message="And today's aid awareness is about, " + urls[b.user_card_count]['text'])
            cron_main_card(b.user_id, urls[b.user_card_count],b)

            return HttpResponse(status=200)


