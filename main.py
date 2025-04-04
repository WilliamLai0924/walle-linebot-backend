from datetime import datetime
from flask import Flask, abort, jsonify, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import PostbackEvent, TextSendMessage, MessageEvent, TextMessage
from apscheduler.schedulers.background import BackgroundScheduler

import requests
import configparser
import os

app = Flask(__name__)
scheduler = BackgroundScheduler()

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

@whhandler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(f'{event}')))


if __name__ == '__main__':
    app.run(debug=True)