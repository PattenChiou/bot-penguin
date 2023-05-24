# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 22:16:59 2021

@author: Patten
"""

import requests, json
import os
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

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

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
def talkToChatGPT(content):
	message = [{"role" : "system", "content" : "You are a counselor whose name is 'Emo'"}, {"role" : "assistant", "content" : "I'm a counselor whose name is 'Emo'"}, {"role" : "user", "content" : content}]
	requestBody = {"model" : "gpt-3.5-turbo",
            "messages" : message,
            "temperature" : 0.9,
            "max_tokens" : 160,
            "frequency_penalty" : 0,
            "presence_penalty" : 0.6
            }
	headers = {"contentType" : "application/json", "Authorization" : "Bearer " + os.getenv("CHATGPT_API_KEY")}
	# print("不是requests.post的問題")
	result = requests.post("https://api.openai.com/v1/chat/completions", headers = headers, json = requestBody)
	# print("是requests.post的問題")
	response = result.json()
	# response = {'id': 'chatcmpl-7ACnqi3uCpOniCcQUZQkaBj2F6hAQ', 'object': 'chat.completion', 'created': 1682666850, 'model': 'gpt-3.5-turbo-0301', 'usage': {'prompt_tokens': 12, 'completion_tokens': 11, 'total_tokens': 23}, 'choices': [{'message': {'role': 'assistant', 'content': '這不是ChatGPT說的：這是一個測試。'}, 'finish_reason': 'stop', 'index': 0}]}
	# print(response)
	return response["choices"][0]["message"]["content"]
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
	chatGPTResponse = talkToChatGPT(msg)
	line_bot_api.reply_message(event.reply_token,TextSendMessage(text=chatGPTResponse))
	# if msg=="AQI":
	# 	#res=getaqi()
	# 	line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入欲查詢城市"))
	# 	lastmsg="AQI"
	# elif lastmsg=="AQI":
	# 	#msg=event.message.text
	# 	"""for i in (0,len(msg)):
	# 		if msg[i]=="A":
	# 			msg=msg[0:i]"""
	# 	res=getaqi(msg)
	# 	line_bot_api.reply_message(event.reply_token,TextSendMessage(text=res))
	# 	lastmsg=msg
	# else:
	# 	#msg=event.message.text
	# 	line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
	# 	lastmsg=event.message.text
if __name__ == "__main__":
    app.run()
    


