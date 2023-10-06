import logging
from telegram import Bot


class LogsHandler(logging.Handler):

    def __init__(self, chat_id, tg_bot_key):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot_key = tg_bot_key

    def emit(self, record):
        log_bot = Bot(token=self.tg_bot_key)
        log_entry = self.format(record)
        log_bot.send_message(text=log_entry, chat_id=self.chat_id)