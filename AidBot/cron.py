from django_cron import CronJobBase, Schedule
from AidBot.views import cron_main_card,post_message
from AidBot.models import BotUser
from django.http import HttpResponse
import json


urls=[{'url':'https://2.sendvid.com/ob29ioyt.mp4','text':'Asthma','description':'Best Practices: \n 1. Help them take their medication \n 2. Reassure the person \n 3. Call the emergency helpline'},{'url':'https://2.sendvid.com/a0xjqwuq.mp4','text':'Heavy Bleeding'},{'url':'https://2.sendvid.com/3qym39uv.mp4','text':'Broken Bones'},{'url':'https://3.sendvid.com/5aofzkew.mp4','text':'Burns'},{'url':'https://1.sendvid.com/j49biv9m.mp4','text':'Choking'},{'url':'https://3.sendvid.com/2nlaza0z.mp4','text':'Diabetes'},{'url':'https://1.sendvid.com/0cbm46t9.mp4','text':'Distress'},{}]

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # 5every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'AidBot.MyCronJob' # a unique code



    def do(self):
        b_user = BotUser.objects.all()
        for b in b_user:

            post_message(b.user_id, message="And today's aid awareness is about, " + urls[b.user_card_count]['text'])
            cron_main_card(b.user_id, urls[b.user_card_count],b)
            post_message(b.user_id,message=urls[b.user_card_count]['description'])

            return HttpResponse(status=200)


