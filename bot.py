from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackContext
)
from dotenv import load_dotenv

import os
import logging
import collections
import pickle


load_dotenv()

def read_subscribers(file_name):
    with open(file_name, 'rb') as subscribers_data:
        return pickle.load(subscribers_data)

def write_subscribers(subscribers, file_name):
    with open(file_name, 'wb') as subscribers_data:
        return pickle.dump(
            subscribers,
            subscribers_data,
            pickle.HIGHEST_PROTOCOL,
        )

if os.path.isfile('subscribers_data.pkl'):
    subscribers = read_subscribers('subscribers_data.pkl')
else:
    subscribers = collections.deque()

updater = Updater(
    token=os.getenv('TELEGRAM_BOT_TOKEN'),
    use_context=True,
)
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

def start(update, context):
    subscribers.append(update.message.chat_id)
    write_subscribers(subscribers, 'subscribers_data.pkl')
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='You\'ve subscribed for stream notifications.',
    )
    print(subscribers)

def stop(update, context):
    subscribers.remove(update.message.chat_id)
    write_subscribers(subscribers, 'subscribers_data.pkl')
    print(subscribers)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)

def start_bot():
    updater.start_polling()
    print('* Starting bot app...')
    print(subscribers)

if __name__ == '__main__':
    start_bot()
