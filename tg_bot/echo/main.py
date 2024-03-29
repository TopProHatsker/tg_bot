from subprocess import Popen
from subprocess import PIPE

from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from echo.config import TG_TOKEN
from echo.config import TG_API_URL


# *************************************************

def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Send me something...",
    )


def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="HELP",
    )


def do_time(bot: Bot, update: Update):
    process = Popen(["date"], stdout=PIPE)
    text, error = process.communicate()
    print("client_get_time")
    if error:
        text = "undefined"
    else:
        text = text.decode("utf-8")

    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
    )


def do_echo(bot: Bot, update: Update):
    text = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
    )


# *************************************************

def main():
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    time_handler = CommandHandler("time", do_time)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print("Start")
    main()
