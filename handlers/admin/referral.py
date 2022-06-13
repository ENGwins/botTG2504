from aiogram import types

from data.message import Name_bot
from keyboards.inline.user import user_cb
from loader import dp, bot
from utils.db_api.db_commands import check_user, check_referral


@dp.callback_query_handler(user_cb.filter(menu='referral'))
async def referral(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    count_referral = await check_referral(str(user_id))
    message = callback
    ref_link = f'https://t.me/{Name_bot}?start={message.from_user.id}'
    await bot.send_message(message.from_user.id, f'<i>Каждый приведенный друг по Вашей ссылке даст Вам</i> <u>50 бонусов!</u>\n'
                                                 f'<i>Если друг совершил заказ, Вам начисляться еще</i> <u>150 бонусов!</u>\n\n'
                                                 f'Нажмите на ссылку, отправьте ее другу и получайте бонусы!\n\n'
                                                 f'<code>{ref_link}</code>\n\n '
                                                 f'<i>Кол-во приведенных друзей:</i> {count_referral}')
    await callback.answer()

    #await bot.send_message(message.from_user.id,f'{total}')


async def check_referral_id(referral_id, user_id):
    if referral_id == '':
        referral_id = '0'
        return referral_id

    elif not referral_id.isnumeric():
        referral_id = '0'
        return referral_id

    elif referral_id.isnumeric():
        if int(referral_id) == user_id:
            referral_id = '0'
            return referral_id
        elif not (await check_user(int(referral_id))):
            referral_id = '0'
            return referral_id
        else:
            referral_id = str(referral_id)
            return referral_id
    else:
        referral_id = '0'
        return referral_id
