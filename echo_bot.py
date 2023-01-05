import os

from environs import Env
from telegram.ext import Updater, MessageHandler, Filters


def echo(update, context):
    update.message.reply_text(update.message.text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    devman_token = env.str('DEVMAN_TOKEN')
    updater = Updater(devman_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()