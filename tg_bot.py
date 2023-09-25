import logging
import dotenv
import os

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from dialogflow_response import dialogflow_response


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)


def start(update: Update, context: CallbackContext):
    logging.info('Command /start')
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def smart_response(update: Update, context: CallbackContext):
    input_text = update.message.text
    session_id = update.effective_chat.id
    response_text, _ = dialogflow_response(project_id, session_id, input_text, language_code)
    context.bot.send_message(chat_id=session_id, text=response_text)


if __name__ == "__main__":
    dotenv.load_dotenv()
    tg_key = os.getenv('TG_BOT_KEY')
    project_id = os.getenv('PROJECT_ID')
    language_code = 'ru-RU'

    updater = Updater(token=tg_key, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    smart_handler = MessageHandler(Filters.text & (~Filters.command), smart_response)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(smart_handler)

    updater.start_polling()
