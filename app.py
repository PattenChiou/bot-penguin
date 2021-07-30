# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 22:16:59 2021

@author: Patten
"""

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	if event.message.text=="==":
		line_bot_api.reply_message(event.reply_token,TextSendMessage("a"))
	else:
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()