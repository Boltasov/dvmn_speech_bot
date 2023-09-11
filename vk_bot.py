import dotenv
import os

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

dotenv.load_dotenv()
vk_key = os.getenv('VK_KEY')
vk_session = vk_api.VkApi(token=vk_key)

longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Новое сообщение:')
        if event.to_me:
            print('Для меня от: ', event.user_id)
        else:
            print('От меня для: ', event.user_id)
        print('Текст:', event.text)