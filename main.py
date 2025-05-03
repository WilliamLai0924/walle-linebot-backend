from datetime import datetime
from flask import Flask, abort, jsonify, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import PostbackEvent, TextSendMessage, MessageEvent, TextMessage

import llm
import requests
import configparser
import os

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = os.environ.get('WALLE_TOKEN', None)
SECRET = os.environ.get('WALLE_SECRET', None)

if TOKEN is None:
    TOKEN = config['linebot']['token']
if SECRET is None:
    SECRET = config['linebot']['secret']

line_bot_api = LineBotApi(TOKEN)
whhandler = WebhookHandler(SECRET)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message':'Hi~'})
  
@app.route('/callback', methods=['POST'])
def callback():
    # 確認請求來自 LINE
    signature = request.headers['X-Line-Signature']

    # 獲取請求主體
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        whhandler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@whhandler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=llm.chat(event.message.text)))

if __name__ == '__main__':
    app.run(debug=True)