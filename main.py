import datetime

import vk_api
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


def write_text_message(sender, message, keyboard=None):
    post = {
        'user_id': sender,
        'message': message,
        'random_id': get_random_id()
    }

    if keyboard != None:
        if kb_step == 'clothes':
            post['keyboard'] = kb_clothes.get_keyboard()
        if kb_step == 'size':
            post['keyboard'] = kb_size.get_keyboard()

    authorize.method('messages.send', post)


token = "vk1.a.TF-4u2teyNARjY5o3Xc-o1wyV9FmLVz0tynbYw8YI6ef3keD7M9nuKJH-yMFAaNUJBgCI1MH2SoMmeH1smqjnT1x7NQTBWNNbJXMJzkf7g3NWGlsijW4gyEJXIUPcas_DT-VLIK6iqea2SMUfchl4BFTswyYU1IaoTrjntsyD23KM9K3rJhwyB0oBpexbJSarK-vUKRIH8-QX3HLGi0BTQ"
authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)
insturction_image = "C:/Users/Azerty/PycharmProjects/pythonProject/dish.jpg"
upload = VkUpload(authorize)
current_time = datetime.datetime.now()
current_hour = current_time.hour
kb_step = None
kb_clothes = VkKeyboard(one_time=False)
kb_clothes.add_button('Худи', color=VkKeyboardColor.PRIMARY)
kb_clothes.add_line()
kb_clothes.add_button('Футболка', color=VkKeyboardColor.PRIMARY)
kb_clothes.add_line()
kb_clothes.add_button('Свитшот', color=VkKeyboardColor.PRIMARY)
kb_clothes.add_line()
kb_clothes.add_button('Шопер', color=VkKeyboardColor.PRIMARY)
clothes_var = ['Худи', 'Футболка', 'Свитшот', 'Шопер']

kb_size = VkKeyboard(one_time=False)
kb_size.add_button('XS', color=VkKeyboardColor.PRIMARY)
kb_size.add_line()
kb_size.add_button('S', color=VkKeyboardColor.PRIMARY)
kb_size.add_line()
kb_size.add_button('M', color=VkKeyboardColor.PRIMARY)
kb_size.add_line()
kb_size.add_button('L', color=VkKeyboardColor.PRIMARY)
kb_size.add_line()
kb_size.add_button('XL', color=VkKeyboardColor.PRIMARY)
size_var = ["XS",  "S", "M", "L", "XL"]
# keyboard1.add_openlink_button('Это Второй ссылка', link='https://rutube.ru/plst/250864/')

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        res_message = event.text
        sender = event.user_id
        # attachments = []
        # upload_image = upload.photo_messages(photos=insturction_image)[0]
        # attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))

        # Приветствие с учетом реального времени
        if current_hour >= 6 and current_hour < 12:
            hel_time = "Доброе утро"
        elif current_hour >= 12 and current_hour < 18:
            hel_time = "Добрый день"
        elif current_hour >= 18 and current_hour < 0:
            hel_time = "Добрый вечер"
        else:
            hel_time = "Доброй ночи"
        if res_message == 'Начать':
            kb_step = 'clothes'
            write_text_message(sender, hel_time + ", выберите одежду из списка:", kb_clothes)
            # Записать данные в файл
        if res_message in clothes_var:
            kb_step = 'size'
            write_text_message(sender, "Выберите размер", kb_size)
        if res_message in size_var:
            write_text_message(sender, "Пришлите в чат картинку с вышивкой")
