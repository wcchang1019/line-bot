from flask import Flask, request, abort
import time
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
CHANNEL_ACCESS_TOKEN = 'SiGEgA71amegCyRbTJ7LkbM+mGrKnpiDnUmgwrcei5T6ozmLcd919xKfzqQO5q0DSKMSgE6XuSy88T36ts3IHgNZRnVVj1KXBuzYhcPFNqvQfuXr1zQzGI1M/lfsnplnmT09NmCgQmRvhNxpjKmdHwdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '7e6fbaa6f8546ec31c586d925deb0c43'
USER_ID = 'U0842cd9c4beca2eda16af2f3fd8988eb'
# Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
    line_bot_api.push_message(USER_ID, TextSendMessage(text='hello world'))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
