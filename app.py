# coding:utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import os
import sys
import csv
import random, string
import re
import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

#import pandas as pd
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('rp98zmyjOxqiY0gXp6rfh24J44UrxZPSz6Mfg+uEtcRRlAXY0NNdO6wlwqcUgbMoI8emfWhwVGnVTsv6azpsxhLqayllgWuQX+Lto76YwilVGmdi+jWZkidn47Kof7nkNLfVESuc3AS7J1KA+n9imwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7e226c6a83c87905a8def19669b71e25')

def movie():
    target_url = 'https://movies.yahoo.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('_slickcontent a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content



# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])

def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


	
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = TextSendMessage(text=event.message.text)

    #line_bot_api.reply_message(event.reply_token, message)
	
    message = event.message.text
    if 'code' in message:
	#random letter and number (secret code generator)	
        s1 = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))
    elif 'Code' in message:
        s1 = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))		
    elif '密碼' in message:
        s1 = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))
    elif 'Roll' in message:
        s1 = ''.join(random.choice(string.digits) for x in range(3)) 			
    elif 'roll' in message:
        s1 = ''.join(random.choice(string.digits) for x in range(3)) 
    elif '最新電影' in message:
        s1 = movie()	
    else:

        lines = [line.strip() for line in open('data.csv')]
        for x in lines:
            match = re.search(message,x)
            if match:
                s1 = x	
                s1 = s1.split(',')[1]
                break	
		

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=s1))
#    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    #line_bot_api.reply_message(event.reply_token, message)

#import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
