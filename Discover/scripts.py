from bs4 import BeautifulSoup
import requests
import json
import re

def get_sub_cards(url):
    cards=[]

    html_content = requests.get(url=url)
    html_content = html_content.text
    soup = BeautifulSoup(html_content, 'html.parser')
    content = soup.select('li.tile.tile--tip')
    for i,list in enumerate(content):
        card={}
        if i==0:
            continue

        title = list.select('div.tileVenue-header')

        for t in title:
            header=t.h4.text
            print header
            card["header"]=header
            category=t.p.text
            print category
            card["category"]=category
            break


        im=list.select('div.tileVenue-content.js-tileVenue-content')

        for i in im:
            try:
                image=i.find('div',style=True)['style']
                urls = re.findall('url\((.*?)\)', image)[0].strip("'")
                image="https://jauntful.com"+urls
                print image

                card["image"]=image
            except:
                card["image"]=" "
            try:
                tip=i.p.text
                card["text"]=tip
                print tip
            except:
                card["text"]=" "
            break

        dir=list.select('div.tileVenue-address')
        for d in dir:
            try:
                directions=d.find('a',href=True)['href']
                print directions

                card["directions"]=directions
            except:
                card["directions"]=" "

            break




        cards.append(card)

    while {} in cards:
        cards.remove({})
    print cards
    return cards

