import logging
import dotenv
import os

from functools import partial
from tg_logger import LogsHandler
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from dialogflow_response import get_dialogflow_response


logger = logging.getLogger("TG logger")


def start(update: Update, context: CallbackContext):
    logging.info('Command /start')
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def get_smart_response(update: Update, context: CallbackContext, project_id, language_code):
    input_text = update.message.text
    session_id = update.effective_chat.id
    response_text, _ = get_dialogflow_response(project_id, session_id, input_text, language_code)
    context.bot.send_message(chat_id=session_id, text=response_text)


def main(tg_key, project_id, language_code):
    updater = Updater(token=tg_key, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    smart_response_enriched = partial(get_smart_response, project_id=project_id, language_code=language_code)
    smart_handler = MessageHandler(
        Filters.text & (~Filters.command),
        smart_response_enriched)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(smart_handler)

    updater.start_polling()


if __name__ == "__main__":
    dotenv.load_dotenv()
    tg_key = os.getenv('TG_BOT_KEY')
    project_id = os.getenv('PROJECT_ID')
    log_bot_key = os.getenv('LOG_BOT_KEY')
    chat_id = os.getenv('CHAT_ID')
    language_code = 'ru-RU'

    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler(chat_id=chat_id, tg_bot_key=log_bot_key))

    try:
        main(tg_key, project_id, language_code)
        logger.info('Speech tg-bot запустился. Всё идёт по плану.')
    except Exception as e:
        logger.exception(f'Speech tg-bot сломался. Лог ошибки:\n {e}')
