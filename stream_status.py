from flask import Flask, request, abort
from bot import dispatcher, CallbackContext, read_subscribers
from telegram.ext.dispatcher import run_async
from telegram.error import Unauthorized
from dotenv import load_dotenv
from datetime import datetime
from twitch_api import TwitchAPI

import json
import requests
import os


load_dotenv()

app = Flask(__name__)

streamer_username = os.getenv('STREAMER_USERNAME')

tw_api = TwitchAPI(os.getenv('TWITCH_CLIENT_ID'))

stream_online = tw_api.is_stream_online(streamer_username)

def twitch_user_link(username):
    return f'twitch.tv/{username}'

@app.route('/stream_changed', methods=['POST', 'GET'])
def stream_changed():
    global stream_online
    if request.method == 'POST':
        streams_data = request.get_json(force=True).get('data')
        if streams_data != [] and stream_online == False:
            stream_online = True
            twitch_streamer_link = twitch_user_link(streamer_username)
            send_notifications(
                read_subscribers('subscribers_data.pkl'),
                f'Stated a stream!\n{twitch_streamer_link}'
            )
        elif streams_data == []:
            stream_online = False
            # send_notifications(read_subscribers('subscribers_data.pkl'), 'Finished a stream.')
        return '', 200
    elif request.method == 'GET':
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\"GET \'/stream_changed\' {now} {request.url}\"')
        return request.args.get('hub.challenge'), 200
    else:
        abort(400)

def send_notifications(subscribers, text):
    for chat_id in subscribers:
        try:
            CallbackContext(dispatcher).bot.send_message(
                chat_id=chat_id,
                text=text
            )
        except Unauthorized as e:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
