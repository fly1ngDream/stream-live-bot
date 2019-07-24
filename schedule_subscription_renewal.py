from stream_status import subscribe_for_stream_changes
from dotenv import load_dotenv

import schedule
import time
import os


load_dotenv()

streamer_username = os.getenv('STREAMER_USERNAME')

schedule.every(8).days.do(
    subscribe_for_stream_changes,
    streamer_username
)

if __name__ == '__main__':
    subscribe_for_stream_changes(streamer_username)
    while True:
        schedule.run_pending()
        time.sleep(60)
