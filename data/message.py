from aiogram import types


#================ Доставка ==========
RUSSIAN_POST_SHIPPING_OPTION = types.ShippingOption(id='ru_post', title='Почтой России')
RUSSIAN_POST_SHIPPING_OPTION.add(types.LabeledPrice('Почта России', 1000))

PICKUP_SHIPPING_OPTION = types.ShippingOption(id='sdec', title='СДЭК')
PICKUP_SHIPPING_OPTION.add(types.LabeledPrice('СДЭК отправление', 1000))


RUSSIAN_POST_SHIPPING_OPTION_BY = types.ShippingOption(
    id='ru_post_by', title='Почтой России')
RUSSIAN_POST_SHIPPING_OPTION_BY.add(types.LabeledPrice('Почта России', 50000))

PICKUP_SHIPPING_OPTION_BY = types.ShippingOption(id='sdec_by', title='СДЭК')
PICKUP_SHIPPING_OPTION_BY.add(types.LabeledPrice('СДЭК отправление', 50000))
#=====================================


dict_for_message_shipping={
    'ru_post':'Почта Росии',
    'ru_post_by':'Почта Росии',
    'sdec':'СДЭК',
    'sdec_by':'СДЭК'
}



ID_PHOTO_MENU='AgACAgIAAxkBAAI1cWKQ2E-M2z5-uid8-57opGEB5KTYAALyvDEbTTSISB6p4fkjqyAfAQADAgADcwADJAQ'