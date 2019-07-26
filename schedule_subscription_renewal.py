from stream_status import subscribe_for_stream_changes
from dotenv import load_dotenv
from twitch_api import TwitchAPI

import schedule
import time
import os


load_dotenv()

streamer_username = os.getenv('STREAMER_USERNAME')

tw_api = TwitchAPI(os.get_env('TWITCH_CLIENT_ID'))

schedule.every(8).days.do(
    tw_api.subscribe_for_stream_changes,
    streamer_username
)

def subscribe_and_schedule_renewal():
    tw_api.subscribe_for_stream_changes(streamer_username)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Gunicorn app object
app = subscribe_and_schedule_renewal

if __name__ == '__main__':
    subscribe_and_schedule_renewal()
