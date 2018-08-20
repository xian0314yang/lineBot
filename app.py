# -*- coding: utf-8 -*-
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
import pandas as pd
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('rp98zmyjOxqiY0gXp6rfh24J44UrxZPSz6Mfg+uEtcRRlAXY0NNdO6wlwqcUgbMoI8emfWhwVGnVTsv6azpsxhLqayllgWuQX+Lto76YwilVGmdi+jWZkidn47Kof7nkNLfVESuc3AS7J1KA+n9imwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7e226c6a83c87905a8def19669b71e25')

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
	
#    message = event.message.text
#    if 'Hello' in message:
#        reply_message = 'World'
#    elif '您好' in message:
#        reply_message = '嗨'
#    else:
#        reply_message = '幹你娘'

#random letter and number (secret code generator)		
#    s1 = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))

    csv_data = pd.read_csv('data.csv') # 讀取訓練資料 
    #print(csv_data.shape) # (189, 9) 
    N = 5 
    csv_batch_data = csv_data.tail(N) # 取後5條資料 
    #print(csv_batch_data.shape) # (5, 9) 
    train_batch_data = csv_batch_data[list(range(3, 6))] # 取這20條資料的3到5列值(索引從0開始) 
    #print(train_batch_data)
		
		
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=train_batch_data))
#    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    #line_bot_api.reply_message(event.reply_token, message)

#import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
