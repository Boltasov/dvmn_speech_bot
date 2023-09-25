import dotenv
import os
import random
import logging

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_response import dialogflow_response


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)


if __name__ == "__main__":
    dotenv.load_dotenv()
    vk_key = os.getenv('VK_KEY')
    project_id = os.getenv('PROJECT_ID')
    language_code = 'ru-RU'

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
