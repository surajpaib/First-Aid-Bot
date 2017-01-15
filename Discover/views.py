from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .scripts import get_sub_cards
import requests
from Discover.models import BotUser
# Create your views here.
import time


ACCESS_TOKEN="EAAPXnZCUZAK4YBAEweO0eZBfht1et6g3XUymUo0drabChPHqr1DY2bSTYN2GcxLt14CUaETSi1mS4Nai8cj37xg5ZByUiSXoGneL6YDfqWMZBuPTDZB4EaOrPIbDNtPZA6dJ5tVkGAClxPp4PuOPAEN59rZArxE5N4T4NWDQOSkzrQZDZD"



def quick_replies(recipient_id):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": "Would you like to Subscribe?",
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

def get_started(recipient_id,body,send_message):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "postback" in message:
                if message["postback"]["payload"]=="start":
                    post_message(recipient_id,send_message)
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
                                post_message(recipient_id,"We'll send you your next new place to explore soon!!")




                        except:

                            b=BotUser.objects.create(user_id=recipient_id,user_card_count=0)

                            post_message(recipient_id,"I'll send you updates about new places everyday. Let's start off with your first one.")
                            with open('card_list.json', 'r') as fp:
                                data = json.load(fp, encoding='utf-8')
                            main_card(recipient_id,data[b.user_card_count])
                            b.save()
                except:
                    print "Not quick reply"



                    #post_message(recipient_id)



def get_recipient_id(body):
    for entry in body['entry']:
        for message in entry['messaging']:
            return message['sender']['id']



def main_card_template(recipient_id,card_data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": card_data["city"],
                            "image_url": card_data["map"],
                            "subtitle": card_data["description"],


                            "buttons":[
                        {
                            "type": "postback",
                            "payload": "city_click",
                            "title": "Discover"
                        }

                    ]

                        }

                    ]
                }
            }
        }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


    print(status.json())


def main_card(recipient_id,card_data):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": card_data["city"],
                            "image_url": card_data["map"],
                            "subtitle": card_data["description"],


                            "buttons":[
                        {
                            "type": "postback",
                            "payload": "click",
                            "title": "Discover"
                        }

                    ]

                        }

                    ]
                }
            }
        }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


    print(status.json())

def cron_main_card(recipient_id,card_data,b):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": card_data["city"],
                            "image_url": card_data["map"],
                            "subtitle": card_data["description"],


                            "buttons":[
                        {
                            "type": "postback",
                            "payload": "cron_click",
                            "title": "Discover"
                        }

                    ]

                        }

                    ]
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



def sub_card_list(recipient_id,url):
    cards=get_sub_cards(url)
    elements=[]
    for card in cards:
        element={
            "title":card["header"],
            "image_url":card["image"],
            "subtitle":card["text"],

            "buttons":[
              {
                "type":"web_url",
                "url":card["directions"],
                "title":"Get there"
              },
                {
                    "type":"element_share"
                }
            ]
          }


        elements.append(element)




    if len(elements)>10:
        elements=elements[0:10]




    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements":


                     elements


                }
            }
        }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)

    print(status.json())


def demo_display(recipient_id,body):
    for entry in body['entry']:
        for message in entry['messaging']:
            if "message" in message:
                try:
                    if message["message"]["quick_reply"]["payload"]=="demo":
                        with open('card_list.json','r') as fp:
                            data=json.load(fp,encoding='utf-8')
                        try:
                            b_user=BotUser.objects.get(user_id=recipient_id)
                            user_card_count=b_user.user_card_count
                            main_card_template(recipient_id,data[user_card_count])
                        except:
                            user_card_count=0
                            main_card_template(recipient_id,data[user_card_count])
                except:
                    if "text" in message["message"]:

                        post_message(recipient_id, message="Let's start discover again, shall we?")
                        time.sleep(5)
                        with open('card_list.json','r') as fp:
                            data=json.load(fp,encoding='utf-8')
                        try:
                            b_user=BotUser.objects.get(user_id=recipient_id)
                            user_card_count=b_user.user_card_count
                            main_card(recipient_id,data[user_card_count])
                        except:
                            user_card_count=0
                            main_card(recipient_id,data[user_card_count])




            elif message["postback"]["payload"]=="city_click":
                with open('card_list.json', 'r') as fp:
                    data = json.load(fp, encoding='utf-8')
                try:
                    b_user = BotUser.objects.get(user_id=recipient_id)
                    user_card_count = b_user.user_card_count
                except:
                    user_card_count=0

                sub_card_list(recipient_id,data[user_card_count]["link"])
                time.sleep(8)
                quick_replies(recipient_id)


            elif message["postback"]["payload"]=="click":
                with open('card_list.json', 'r') as fp:
                    data = json.load(fp, encoding='utf-8')
                try:
                    b_user = BotUser.objects.get(user_id=recipient_id)
                    user_card_count = b_user.user_card_count
                except:
                    user_card_count=0

                sub_card_list(recipient_id, data[user_card_count]["link"])
                time.sleep(8)
                post_message(recipient_id, message="All done for now! Let's explore more tomorrow")


            elif message["postback"]["payload"] == "cron_click":
                with open('card_list.json', 'r') as fp:
                    data = json.load(fp, encoding='utf-8')
                try:
                    b_user = BotUser.objects.get(user_id=recipient_id)
                    user_card_count = b_user.user_card_count - 1
                except:
                    user_card_count = 0


                sub_card_list(recipient_id,data[user_card_count]["link"])
                time.sleep(8)
                post_message(recipient_id,message="All done for now! Let's explore more tomorrow")


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



        get_started_message="Hello! I love exploring new places and things to do. I'll send you updates everyday about whatever I find!"

        get_started(recipient_id,body,get_started_message)

        ''' Three possible flows after Get Started option'''
        subscribe(recipient_id,body)


        demo_display(recipient_id,body)
        return HttpResponse(status=200)
























