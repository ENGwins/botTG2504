import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp
from states.Mailing import MailingService


# =================================Рассылка=================================


# функция рассылки сообщений
@dp.message_handler(state=MailingService.text)
async def mailing_text(message: types.Message, state: FSMContext):
    # await bot.send_message(message.from_user.id, 'Рассылка начата!')
    answer = message.text
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='📷Добавить фотографию', callback_data='add_photo'),
                                          InlineKeyboardButton(text='📩Отправить', callback_data='next'),
                                          InlineKeyboardButton(text='🗙Отменить', callback_data='quit')
                                      ]
                                  ])
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=markup)
    await MailingService.state.set()


@dp.message_handler(state=MailingService.photo, content_types=types.ContentTypes.PHOTO)
async def mailing_photo(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id  # возвращает файл id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='📩Отправить', callback_data='next'),
                                          InlineKeyboardButton(text='🗙Отменить', callback_data='quit')

                                      ]
                                  ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)

@dp.message_handler(state=MailingService.photo)
async def no_photo(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='🗙Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer('Пришли мне фотографию', reply_markup=markup)
