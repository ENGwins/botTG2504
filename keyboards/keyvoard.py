from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

bt5_0=KeyboardButton('Да')
bt5_1=KeyboardButton('Ввести заново')
bt5_2=KeyboardButton('Изменить')
kb_yes_no=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(bt5_0, bt5_1)

bt4_0=KeyboardButton('Начать вводить')
bt4_1=KeyboardButton('Изменение размеров')
bt4_2=KeyboardButton('Главное меню')
kb_size=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(bt4_0,bt4_2)
kb_start_size=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(bt4_1,bt4_2)

# -----Main menu---- 0

bt0_1 = KeyboardButton('Давай познакомимся')
bt0_2 = KeyboardButton('Каталог')
bt0_3 = KeyboardButton('Как сделать заказ')
bt0_4 = KeyboardButton('Доставка')
bt0_5 = KeyboardButton('Личная информация')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(bt0_1, bt0_2, bt0_3, bt0_4).insert(bt0_5)

sizeMain=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(bt5_1,bt4_2)