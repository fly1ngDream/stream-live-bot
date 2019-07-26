from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackContext
)
from telegram.ext.dispatcher import run_async
from dotenv import load_dotenv

import os
import logging
import collections
import pickle


load_dotenv()

def read_subscribers(file_name):
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as subscribers_data:
            return pickle.load(subscribers_data)
    else:
        return collections.deque()

def write_subscribers(subscribers, file_name):
    with open(file_name, 'wb') as subscribers_data:
        pickle.dump(
            subscribers,
            subscribers_data,
            pickle.HIGHEST_PROTOCOL,
        )

subscribers = read_subscribers('subscribers_data.pkl')

updater = Updater(
    token=os.getenv('TELEGRAM_BOT_TOKEN'),
    use_context=True,
)
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

@run_async
def start(update, context):
    chat_id = update.message.chat_id
    if not chat_id in subscribers:
        subscribers.append(chat_id)
        write_subscribers(subscribers, 'subscribers_data.pkl')
        print(subscribers)
        context.bot.send_message(
            chat_id=chat_id,
            text='You\'ve subscribed for stream notifications.',
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='You are already subscribed.',
        )

@run_async
def stop(update, context):
    chat_id = update.message.chat_id
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        write_subscribers(subscribers, 'subscribers_data.pkl')
        print(subscribers)
        context.bot.send_message(
            chat_id=chat_id,
            text='You\'ve unsubscribed.',
        )
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='You are not subscribed.',
        )

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
