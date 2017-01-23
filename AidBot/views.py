from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from AidBot.messenger_functions import get_recipient_id,demo_display,subscribe,get_started









def verify_token(request):
    if (request.GET['hub.verify_token'] == "discover"):
        return HttpResponse(request.GET['hub.challenge'],status=200)
    else:
        return HttpResponse("Wrong verification token",status=200)






'''

Main Code and Bot Flow

'''
@csrf_exempt
def webhook(request):
    if request.method=="GET":
        return verify_token(request)

    if request.method=="POST":


        body=json.loads(request.body.decode('utf-8'))
        recipient_id=get_recipient_id(body)



        get_started_message="Hey! Welcome to First Aid Bot. I'll help you learn best practices for what to do in an emergency and provide, First Aid"


        get_started(recipient_id,body,get_started_message)

        ''' Three possible flows after Get Started option'''

        demo_display(recipient_id,body)

        return HttpResponse(status=200)
























