from flask import Flask, request, abort
from bot import dispatcher, CallbackContext, read_subscribers
from dotenv import load_dotenv
from datetime import datetime

import json
import requests
import os


load_dotenv()

app = Flask(__name__)

@app.route('/stream_changed', methods=['POST', 'GET'])
def stream_changed():
    if request.method == 'POST':
        streams_data = request.get_json(force=True).get('data')
        if streams_data != []:
            send_notifications(read_subscribers('subscribers_data.pkl'))
        return '', 200
    elif request.method == 'GET':
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\"GET \'/stream_changed\' {now}\"')
        return '', 200
    else:
        abort(400)

def send_notifications(subscribers):
    for chat_id in subscribers:
        CallbackContext(dispatcher).bot.send_message(
            chat_id=chat_id,
            text='Started a stream!'
        )

def subscribe_for_stream_changes(user_id):
    url = 'https://api.twitch.tv/helix/webhooks/hub'
    ip = os.getenv('IP')
    hub_data = {
        'hub.callback': f'http://{ip}:8000/stream_changed',
        'hub.mode': 'subscribe',
        'hub.topic': f'https://api.twitch.tv/helix/streams?user_id={user_id}',
    }
    headers = {
        'Client-ID': os.getenv('TWITCH_CLIENT_ID'),
    }
    requests.post(
        url,
        json=hub_data,
        headers=headers,
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    # subscribe_for_stream_changes()