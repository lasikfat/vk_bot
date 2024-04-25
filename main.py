import datetime
import sqlite3

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
        if k_step == 'clothes':
            post['keyboard'] = kb_clothes.get_keyboard()
        if k_step == 'size':
            post['keyboard'] = kb_size.get_keyboard()

    authorize.method('messages.send', post)


def fixMes(res_message):
    res_message = "'" + res_message + "'"
    return res_message


token = "vk1.a.TF-4u2teyNARjY5o3Xc-o1wyV9FmLVz0tynbYw8YI6ef3keD7M9nuKJH-yMFAaNUJBgCI1MH2SoMmeH1smqjnT1x7NQTBWNNbJXMJzkf7g3NWGlsijW4gyEJXIUPcas_DT-VLIK6iqea2SMUfchl4BFTswyYU1IaoTrjntsyD23KM9K3rJhwyB0oBpexbJSarK-vUKRIH8-QX3HLGi0BTQ"
authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)
insturction_image = "C:/Users/Azerty/PycharmProjects/pythonProject/dish.jpg"

k_step = ''

txt = open('check_list.txt', 'r+')

db = sqlite3.connect('action.db')
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users (
    userID BIGINT,
    date TEXT,
    act TEXT,
    fio TEXT,
    adres TEXT,
    clothes TEXT,
    size TEXT
)""")
db.commit()

userAct = '0'

upload = VkUpload(authorize)
current_time = datetime.datetime.now()
current_hour = current_time.hour


var_go = ['регистрация']
kb_var = VkKeyboard(one_time=False)
kb_var.add_button(var_go[0], color=VkKeyboardColor.POSITIVE)


var_zak = ['сделать заказ']
kb_zak = VkKeyboard(one_time=False)
kb_zak.add_button(var_zak[0], color=VkKeyboardColor.POSITIVE)


clothes_var = ['худи', 'футболка', 'свитшот', 'шопер']
kb_clothes = VkKeyboard(one_time=False)
kb_clothes.add_button(clothes_var[0], color=VkKeyboardColor.PRIMARY)
kb_clothes.add_line()
kb_clothes.add_button(clothes_var[1], color=VkKeyboardColor.PRIMARY)
kb_clothes.add_line()
kb_clothes.add_button(clothes_var[2], color=VkKeyboardColor.PRIMARY)
kb_clothes.add_line()
kb_clothes.add_button(clothes_var[3], color=VkKeyboardColor.PRIMARY)

size_var = ["xl", "s", "m", "l", "Xl"]
kb_size = VkKeyboard(one_time=False)
kb_size.add_button(size_var[0], color=VkKeyboardColor.PRIMARY)
kb_size.add_line()
kb_size.add_button(size_var[1], color=VkKeyboardColor.PRIMARY)
kb_size.add_line()
kb_size.add_button(size_var[2], color=VkKeyboardColor.PRIMARY)
kb_size.add_line()
kb_size.add_button(size_var[3], color=VkKeyboardColor.PRIMARY)
kb_size.add_line()
kb_size.add_button(size_var[4], color=VkKeyboardColor.PRIMARY)

if current_hour >= 6 and current_hour < 12:
    hel_time = "Доброе утро"
elif current_hour >= 12 and current_hour < 18:
    hel_time = "Добрый день"
elif current_hour >= 18 and current_hour < 0:
    hel_time = "Добрый вечер"
else:
    hel_time = "Доброй ночи"

# keyboard1.add_openlink_button('Это Второй ссылка', link='https://rutube.ru/plst/250864/')

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        res_message = event.text.lower()
        sender = event.user_id
        cur.execute(f"SELECT userID FROM users WHERE userID = '{sender}'")
        if cur.fetchone() is None:
            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (sender, "0", "newUser", "0", "0", "0", "0"))
            db.commit()
            k_step = 'go'
            write_text_message(sender,
                               hel_time + ", приветствуем вас в нашей студии. Я бот-помощник. Помогу вам со всеми вопросами. Если ты впервые, то быстрее регистрируйся!")
        else:
            userAct = cur.execute(f"SELECT act FROM users WHERE userID = '{sender}'").fetchone()[0]
            if userAct == "newUser" and res_message == 'регистрация':
                write_text_message(sender, "Давай познакомимся, а потом сделаем заказ. Как тебя зовут? Напиши свое ФИ",)
                cur.execute(f"UPDATE users SET act = 'get_fio' WHERE userID = {sender}")
                db.commit()
            elif userAct == 'get_fio':
                cur.execute(f"UPDATE users SET fio = {fixMes(res_message)} WHERE userID = {sender}")
                cur.execute(f"UPDATE users SET act = 'get_adres' WHERE userID = {sender}")
                db.commit()
                write_text_message(sender, "Где ты живешь? Для того, чтобы мы знали куда доставить твой заказ")
            elif userAct == "get_adres":
                cur.execute(f"UPDATE users SET adres = {fixMes(res_message)} WHERE userID = {sender}")
                cur.execute(f"UPDATE users SET act = 'zakaz' WHERE userID = {sender}")
                db.commit()
                write_text_message(sender,
                                   "Ура! Теперь мы с тобой знакомы, если ты хочешь узнать о нас, то можешь посмотреть нашу группу. Там много интересного. Чтобы сделать заказ просто нажми кнопку Сделать заказ",)
            elif userAct == "zakaz" and res_message == 'сделать заказ':
                cur.execute(f"UPDATE users SET act = 'get_clothes' WHERE userID = {sender}")
                db.commit()
                kb_var = 'clothes'
                write_text_message(sender, "Выбери одежду на которой ты хочешь вышивку", kb_clothes)
            elif userAct == 'get_clothes' and res_message in clothes_var:
                cur.execute(f"UPDATE users SET clothes = {fixMes(res_message)} WHERE userID = {sender}")
                cur.execute(f"UPDATE users SET act = 'get_size' WHERE userID = {sender}")
                db.commit()
                kb_var = 'size'
                write_text_message(sender, "Осталось совсем чуть чуть! Выбери размер одежды", kb_size)
            elif userAct == 'get_size' and res_message in size_var:
                cur.execute(f"UPDATE users SET size = {fixMes(res_message)} WHERE userID = {sender}")
                cur.execute(f"UPDATE users SET act = 'get_emb' WHERE userID = {sender}")
                db.commit()
                write_text_message(sender, "Опишите вышивку или пришлите фото!")
            elif userAct == 'get_emb':
                write_text_message(sender,
                                   "Спасибо за заказ! Я все записал и передам нашему администратору, он скоро свяжется с вами!",)


txt.close()
