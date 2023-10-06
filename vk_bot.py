import dotenv
import os
import random
import logging

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from tg_logger import LogsHandler

from dialogflow_response import dialogflow_response


logger = logging.getLogger("TG logger")


def main(vk_key, project_id, language_code):
    vk_session = vk.VkApi(token=vk_key)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            session_id = event.user_id
            input_text = event.text
            response_text, is_fallback = dialogflow_response(project_id, session_id, input_text, language_code)
            if not is_fallback:
                vk_api.messages.send(user_id=session_id, message=response_text, random_id=random.randint(0, 1023))


if __name__ == "__main__":
    dotenv.load_dotenv()
    vk_key = os.getenv('VK_KEY')
    project_id = os.getenv('PROJECT_ID')
    language_code = 'ru-RU'
    log_bot_key = os.getenv('LOG_BOT_KEY')
    chat_id = os.getenv('CHAT_ID')

    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler(chat_id=chat_id, tg_bot_key=log_bot_key))

    try:
        main(vk_key, project_id, language_code)
        logger.info('Speech vk-bot запустился. Всё идёт по плану.')
    except Exception as e:
        logger.exception(f'Speech vk-bot сломался. Лог ошибки:\n {e}')
