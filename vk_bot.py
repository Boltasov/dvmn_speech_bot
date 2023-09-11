import dotenv
import os
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_response import dialogflow_response


dotenv.load_dotenv()
tg_key = os.getenv('TG_BOT_KEY')
project_id = os.getenv('PROJECT_ID')
language_code = 'ru-RU'


def info(vk_key):
    vk_session = vk.VkApi(token=vk_key)
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    dotenv.load_dotenv()
    vk_key = os.getenv('VK_KEY')
    vk_session = vk.VkApi(token=vk_key)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            session_id = event.user_id
            input_text = event.text
            response_text, is_fallback = dialogflow_response(project_id, session_id, input_text, language_code)
            if not is_fallback:
                vk_api.messages.send(user_id=session_id, message=response_text, random_id=0)
