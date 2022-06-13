from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import emoji

bt5_0=KeyboardButton('Да')
bt5_1=KeyboardButton('Ввести заново')
bt5_2=KeyboardButton('Изменить')
kb_yes_no=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(bt5_0, bt5_1)

bt4_0=KeyboardButton('Начать вводить')
bt4_1=KeyboardButton('Изменение размеров')
bt4_2=KeyboardButton('Главное меню')
bt4_3=KeyboardButton('Назад')
kb_size=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(bt4_0,bt4_3)
kb_start_size=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(bt4_1,bt4_3)

# -----Main menu---- 0

bt0_1 = KeyboardButton('О нас')
bt0_2 = KeyboardButton(text=emoji.emojize(':scroll:')+ 'Каталог')
bt0_3 = KeyboardButton('❓ Как сделать заказ')
bt0_4 = KeyboardButton(text=emoji.emojize(':rocket:')+ 'Доставка')
bt0_5 = KeyboardButton(text=emoji.emojize(':woman_frowning:')+ 'Личный кабинет')
bt0_6 = KeyboardButton(text='₽ Бонусы')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(bt0_2).insert(bt0_5).add(bt0_4,bt0_6,bt0_1).insert(bt0_3)

sizeMain=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(bt5_1,bt4_2)

