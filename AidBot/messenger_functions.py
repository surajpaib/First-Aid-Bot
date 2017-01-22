from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from AidBot.models import BotUser
# Create your views here.
from AidBot.witclient import wit_client
from AidBot.data import get_urls





ACCESS_TOKEN="EAAIwbZBDYzr8BANC8jCOpFZBqDmx6oM7nCG4UWmNxS5ijZAIJ0j8ZBs9qkG6L7ki0ZADf06oPl1zgAmSM4hxkPXJO7q5Ij0k5S0IUcygRGa5G5J7dvja7JAnB35ZAofQa2vqYPtD3nIXZCaX1TlZBK235CkAMp7wsvuhZCDj2klzFNQZDZD"

urls=get_urls()


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
                                post_message(recipient_id,"You've already subscribed with us!!")





                        except:

                            b=BotUser.objects.create(user_id=recipient_id,user_card_count=0)

                            post_message(recipient_id,"I'll send you updates everyday. Let's start off with your first one.")
                            post_message(recipient_id,message="Today, we're going to learn a bit about " + urls[b.user_card_count]['text'])
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

    quick_replies(recipient_id)
    print(status.json())









def main_card(recipient_id,card_data):
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

    button(recipient_id,"Video Credits: British Red Cross. Make sure you find the right Emergency Helpline for your Country","https://en.wikipedia.org/wiki/List_of_emergency_telephone_numbers")

    print(status.json())










def button(recipient_id,text,url):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({
  "recipient":{
    "id":recipient_id
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":text,
        "buttons":[
          {
            "type":"web_url",
            "url":url,
            "title":"Show Website",
            "webview_height_ratio":"compact"
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
                "type": "video",
                "payload": {
                    "url":card_data["url"]
                }
            }
        }
    })


    b.user_card_count+=1
    b.save()
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    button(recipient_id,
           "Video Credits: British Red Cross. Make sure you find the right Emergency Helpline for your Country",
           "https://en.wikipedia.org/wiki/List_of_emergency_telephone_numbers")
    button(recipient_id)

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
                            post_message(recipient_id, message="Today, we learn a bit about " + urls[user_card_count]["text"])
                            main_card_template(recipient_id,urls[user_card_count])
                        except:
                            user_card_count=0
                            post_message(recipient_id,message="Today, we learn a bit about " + urls[user_card_count]["text"])
                            main_card_template(recipient_id,urls[user_card_count])

                        b_user.user_card_count+=1
                        b_user.save()

                        return HttpResponse(status=200)
                except:
                    if "text" in message["message"]:
                        response=wit_client(message["message"]["text"])
                        for url in urls:
                            if url['title'].lower() ==response:
                                post_message(recipient_id,url['desc'])
                                break
                        return HttpResponse(status=200)

            elif "postback" in message:
                if message["postback"]["payload"]=="help":
                    try:
                            mes="First Aid Bot sends you updates daily about different situations and how you can effectively offer primary aid. \nYou can also enter a situation scenario and I'll offer you suggestions and best practices. You can also try the first aid Quiz in the Menu to see how good you've gotten "
                            post_message(recipient_id,mes)
                            return HttpResponse(status=200)
                    except:

                            return HttpResponse(status=200)



                elif message["postback"]["payload"]=="search":
                    try:
                            mes="Describe to First Aid Bot your situation and I'll analyze it for you and give you tips on providing aid"
                            post_message(recipient_id,mes)
                            return HttpResponse(status=200)
                    except:
                            return HttpResponse(status=200)

                elif message["postback"]["payload"]=="quiz":
                    try:
                            mes="Currently a Work in Progress!"
                            post_message(recipient_id,mes)
                            return HttpResponse(status=200)
                    except:
                            return HttpResponse(status=200)

