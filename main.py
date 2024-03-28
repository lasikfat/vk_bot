import datetime
import vk_api
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


def write_message(sender, message):
    authorize.method('messages.send', {'user_id': sender, 'message': message, "random_id": get_random_id()})


# 'user_id': sender, 'message': message, "random_id": get_random_id(),'attachment': ','.join(attachments), 'keyboard': keyboard.get_keyboard()


token = "vk1.a.TF-4u2teyNARjY5o3Xc-o1wyV9FmLVz0tynbYw8YI6ef3keD7M9nuKJH-yMFAaNUJBgCI1MH2SoMmeH1smqjnT1x7NQTBWNNbJXMJzkf7g3NWGlsijW4gyEJXIUPcas_DT-VLIK6iqea2SMUfchl4BFTswyYU1IaoTrjntsyD23KM9K3rJhwyB0oBpexbJSarK-vUKRIH8-QX3HLGi0BTQ"
authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)
insturction_image = "C:/Users/Azerty/PycharmProjects/pythonProject/dish.jpg"
upload = VkUpload(authorize)
current_time = datetime.datetime.now()
current_hour = current_time.hour
keyboard1 = VkKeyboard(one_time=True)
keyboard1.add_button('Худи', color=VkKeyboardColor.PRIMARY)
keyboard1.add_line()
keyboard1.add_button('Футболка', color=VkKeyboardColor.PRIMARY)
keyboard1.add_line()
keyboard1.add_button('Свитшот', color=VkKeyboardColor.PRIMARY)
keyboard1.add_line()
keyboard1.add_button('Шопер', color=VkKeyboardColor.PRIMARY)
#keyboard1.add_openlink_button('Это Второй ссылка', link='https://rutube.ru/plst/250864/')

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        res_message = event.text
        sender = event.user_id
        attachments = []
        upload_image = upload.photo_messages(photos=insturction_image)[0]
        attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))

        # Приветствие с учетом реального времени
        if current_hour >= 6 and current_hour < 12:
            hel_time = "Доброе утро"
        elif current_hour >= 12 and current_hour < 18:
            hel_time = "Добрый день"
        elif current_hour >= 18 and current_hour < 0:
            hel_time = "Добрый вечер"
        else:
            hel_time = "Доброй ночи"
        write_message(sender, hel_time + ", для заказа нам потребуются ваши данные")
        write_message(sender, keyboard1.get_keyboard())


