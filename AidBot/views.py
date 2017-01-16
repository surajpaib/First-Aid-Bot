from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .scripts import get_sub_cards
import requests
from AidBot.models import BotUser
# Create your views here.
import time


ACCESS_TOKEN="EAAIwbZBDYzr8BANC8jCOpFZBqDmx6oM7nCG4UWmNxS5ijZAIJ0j8ZBs9qkG6L7ki0ZADf06oPl1zgAmSM4hxkPXJO7q5Ij0k5S0IUcygRGa5G5J7dvja7JAnB35ZAofQa2vqYPtD3nIXZCaX1TlZBK235CkAMp7wsvuhZCDj2klzFNQZDZD"


urls=[{'url':'https://2.sendvid.com/ob29ioyt.mp4','text':'Asthma'},{'url':'https://2.sendvid.com/a0xjqwuq.mp4','text':'Heavy Bleeding'}]


def quick_replies(recipient_id):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": "I'll send you updates daily. Would you like to Subscribe?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Yes",
                    "payload": "yes"
                },
                {
                    "content_type": "text",
                    "title": "View Demo",
                    "payload": "demo"
                }
            ]
        }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())

def get_started(recipient_id,body,send_message,message2):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "postback" in message:
                if message["postback"]["payload"]=="start":
                    post_message(recipient_id,send_message)
                    post_message(recipient_id,message2)
                    quick_replies(recipient_id)


def subscribe(recipient_id,body):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "message" in message:
                try:
                    if message["message"]["quick_reply"]["payload"]=="yes":
                        try:
                            b_exists=BotUser.objects.get(user_id=recipient_id)
                            if recipient_id==b_exists.user_id:
                                b_exists.user_card_count+=1
                                b_exists.save()
                                post_message(recipient_id,"You've already subscribed with us!!")





                        except:

                            b=BotUser.objects.create(user_id=recipient_id,user_card_count=0)

                            post_message(recipient_id,"I'll send you updates everyday. Let's start off with your first one.")

                            main_card(recipient_id,urls[b.user_card_count])
                            b.save()
                except:
                    print "Not quick reply"



                    #post_message(recipient_id)



def get_recipient_id(body):
    for entry in body['entry']:
        for message in entry['messaging']:
            return message['sender']['id']



def main_card_template(recipient_id,card_data):
    post_message(recipient_id,message="Today, we learn a bit about "+card_data["text"])
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "video",
                "payload": {
                    "url":card_data['url']
                }
            }
        }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


    print(status.json())


def main_card(recipient_id,card_data):
    post_message(recipient_id,message="Today, we're going to learn a bit about "+card_data['text'])
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "video",
                "payload": {
                    "url":card_data['url']
                }
            }
        }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


    print(status.json())

def cron_main_card(recipient_id,card_data,b):
    post_message(recipient_id,message="And today's aid awareness is about, "+card_data['text'])
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "video",
                "payload": {
                    "url":card_data['url']
                }
            }
        }
    })


    b.user_card_count+=1
    b.save()
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


    print(status.json())


def post_message(recipient_id,message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": recipient_id}, "message": {"text": message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())





def demo_display(recipient_id,body):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "message" in message:
                try:
                    if message["message"]["quick_reply"]["payload"]=="demo":
                        try:
                            b_user=BotUser.objects.get(user_id=recipient_id)
                            user_card_count=b_user.user_card_count
                            main_card_template(recipient_id,urls[user_card_count])
                        except:
                            user_card_count=0
                            main_card_template(recipient_id,urls[user_card_count])

                        b_user.user_card_count+=1
                        b_user.save()

                except:
                    if "text" in message["message"]:
                        if message["message"]["text"]=="help" or message["message"]["text"]=="Help" or  message["message"]["text"]=="HELP":

                            post_message(recipient_id, message="I'll send you video content everyday about providing aid for different situations. I hope to gear you up!")
                            return HttpResponse(status=200)







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

        get_started_message2="Thousands of people are dying each year in situations where first aid could have made the difference,this includes nearly 900 people who choke to death, 2500 who asphyxiate from a blocked airway and 29000 who die from heart attacks."

        get_started(recipient_id,body,get_started_message,get_started_message2)

        ''' Three possible flows after Get Started option'''
        subscribe(recipient_id,body)


        demo_display(recipient_id,body)
        return HttpResponse(status=200)
























