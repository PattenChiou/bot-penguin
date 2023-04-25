# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 22:16:59 2021

@author: Patten
"""

import requests
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Jy/ZzuRD+p9OpnjsUDgxenc+p2eUOcMBFzkRar2ktv9KvBBskzVo2ElbWgjJV8SqFiOHpz4ly7THIjD78+t8a8VP6rzA1HV1cEKiw7lwzvicbpLR8khk6e0nbRH3Kk1WpD7b3MAdPIi9NppErT2OOAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3b49855fa281d4d63dfe85bb9cb24f1e')

def getaqi(x):
	str1=""
	r=requests.get("https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON")
	content=r.json()
	for i in range(0,len(content["records"])):
		if content["records"][i]["sitename"]==x or content["records"][i]["county"]==x :
			str1 += content["records"][i]["sitename"] + "：" + content["records"][i]["aqi"] + " 指標污染物：" + content["records"][i]["pollutant"] + "\n" + "(%s)"%content["records"][i]["publishtime"] + "\n"
	if len(str1)==0:
		return "查無資料"
	else:
		return str1
#a=getaqi()
#print(a)
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

msg=""
lastmsg=""

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	global msg
	global lastmsg
	msg=event.message.text
	if msg=="AQI":
		#res=getaqi()
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入欲查詢城市"))
		lastmsg="AQI"
	elif lastmsg=="AQI":
		#msg=event.message.text
		"""for i in (0,len(msg)):
			if msg[i]=="A":
				msg=msg[0:i]"""
		res=getaqi(msg)
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res))
		lastmsg=msg
	else:
		#msg=event.message.text
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
		lastmsg=event.message.text
if __name__ == "__main__":
    app.run()
    


