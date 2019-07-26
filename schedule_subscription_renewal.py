from dotenv import load_dotenv
from twitch_api import TwitchAPI

import schedule
import time
import os


load_dotenv()

streamer_username = os.getenv('STREAMER_USERNAME')

tw_api = TwitchAPI(os.getenv('TWITCH_CLIENT_ID'))

schedule.every(8).days.do(
    tw_api.subscribe_for_stream_changes,
    streamer_username
)

def sleep(seconds):
    for i in range(seconds):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            continue

if __name__ == '__main__':
    tw_api.subscribe_for_stream_changes(streamer_username)
    while True:
        schedule.run_pending()
        sleep(60)
