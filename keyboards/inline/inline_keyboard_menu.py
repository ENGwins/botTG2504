from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu=InlineKeyboardMarkup(row_width=2,
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(text='Сообщение',callback_data='Сообщение'),
                                      InlineKeyboardButton(text='Ссылка',url='https://yandex.ru')
                                  ],
                                  [
                                      InlineKeyboardButton(text='aletr', callback_data='alert')
                                  ]
                              ])