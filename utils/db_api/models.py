import asyncio

from utils.db_api.db_commands import add_item


async def add_items():
    await add_item(name='PARADISE персиковый',
                   category_name='Комплект на косточках', category_code='Kost',
                   subcategory_name='PARADISE', subcategory_code='paradise',
                   decription='Шикарный персиковый комплект Paradise выполнен из вышивки на сетке, изделия из этого материала являются более износостойкими чем кружевные\n'
                              '\n'
                              '•чашечки имеют подкладку из сеточки для комфортной носки;\n'
                              '•трусики могут быть стринги или стринги на регуляторах;\n'
                              '\n'
                              '75A, 80A '
                              '70B, 75B, 80B, 85B \n'
                              '70C, 75C, 80C \n'
                              'XS, S, M, L, XL',
                   price=4590,
                   photo="AgACAgIAAxkBAAIngGJ8HeS03uoV0CAvM_c0FojxZvvgAAJquTEbcAboS9Jl5IykhiVIAQADAgADcwADJAQ"
                   )

    await add_item(name='GROW турецкая сеточка + кружево',
                   category_name='Комплект на косточках', category_code='Kost',
                   subcategory_name='GROW', subcategory_code='grow',
                   decription='Роскошное сочетание песочной сеточки и изумрудного кружева✨\n'
                              '• лиф с косточками, поверх чашечки из турецкой сеточки проходит изумрудное кружево;\n'
                              '• трусики стринги на высокой посаде;\n'
                              '\n'
                              '75A, 80A\n'
                              '70B, 75B, 80B, 85B\n'
                              '70C, 75C, 80C \n'
                              '\n'
                              'XS, S, M, L, XL',
                   price=3000,
                   photo="AgACAgIAAxkBAAInfmJ8HQ_Roq3WKM2ujO4TwvDzL1DuAAJmuTEbcAboS53al3QJCbbRAQADAgADcwADJAQ"
                   )

    """    await add_item(name='WOW в красном цвете',
                   category_name='Комплет с т-чашкой', category_code='ch',
                   subcategory_name='WOW', subcategory_code='wow',
                   decription='Лиф с т-чашкой и декоративными резиночками над чашкой, под основанием лифа (длина регулируется)\n'
                              '+ трусики стринги средняя или высокая посадка\n'
                              'Сеточка от турецкого производителя, мягкая и хорошо тянется,\n'
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              '75D\n '
                              'XS, S, M, L, XL\n',
                   price=3990,
                   photo="AgACAgIAAxkBAAInamJ8FKhz6RmM2O6qd8Vi1vdprHEoAAJsvjEbcAbgS3TFQo__KX2pAQADAgADcwADJAQ"
                   )

    await add_item(name='WOW в чёрном цвете',
                   category_name='Комплет с т-чашкой', category_code='ch',
                   subcategory_name='WOW', subcategory_code='wow',
                   decription='Лиф с т-чашкой и декоративными резиночками над чашкой, под основанием лифа (длина регулируется)\n'
                              '+ трусики стринги средняя или высокая посадка\n'
                              'Сеточка от турецкого производителя, мягкая и хорошо тянется,\n'
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              '75D\n '
                              'XS, S, M, L, XL\n',
                   price=3990,
                   photo="AgACAgIAAxkBAAInbGJ8FzBeJlJppMWKWhvYf2qf2EnhAAJ7vjEbcAbgS9k8oCrHkHrsAQADAgADcwADJAQ"
                   )

    await add_item(name='Пудровый',
                   category_name='Комплект без косточек', category_code='noKost',
                   subcategory_name='Base', subcategory_code='base',
                   decription='Лиф + трусики стринги высокая или средняя посадка\n'
                              'Комплект выполнен из мягкой сеточки, идеально подойдёт для каждодневной носки.\n '
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=990,
                   photo="AgACAgIAAxkBAAInbmJ8F_pE3uCQxx8HYp_WdCjNCcsOAAJ-vjEbcAbgS5WaONwuOjDaAQADAgADcwADJAQ"
                   )

    await add_item(name='Желтый',
                   category_name='Комплект без косточек', category_code='noKost',
                   subcategory_name='LOW', subcategory_code='low',
                   decription='Комплект выполнен из мягкого кружева, лиф имеет низкую чашку и придает груди округлую форму.\n '
                              'Трусики двух видов — стринги и танга на регуляторах.\n'
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=2990,
                   photo="AgACAgIAAxkBAAIncGJ8GKwn1aTDqHZbBZ_MWTUv-Q1jAAJZuTEbcAboSxMhRxXvjV8lAQADAgADcwADJAQ"
                   )

    await add_item(name='Туманно-голубой',
                   category_name='Комплект без косточек', category_code='noKost',
                   subcategory_name='LOW', subcategory_code='low',
                   decription='Комплект выполнен из мягкого кружева, лиф имеет низкую чашку и придает груди округлую форму.\n '
                              'Трусики двух видов — стринги и танга на регуляторах.\n'
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=2990,
                   photo="AgACAgIAAxkBAAIncmJ8GOisq3NNWXPw7Xi257Bu8jggAAJauTEbcAboS98uwaeB6AwaAQADAgADcwADJAQ"
                   )

    await add_item(name='Fly черный',
                   category_name='Комплект без косточек', category_code='noKost',
                   subcategory_name='Fly', subcategory_code='fly',
                   decription='Комплект с лифом без косточек + трусики бразилиана \n'
                              'Отличный вариант для тех, кто не любит косточки в бюстгальтерах. Лиф fly имеет плотную ленту под чашечкой, что позволяет придерживать даже большой объём груди. \n '
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=2500,
                   photo="AgACAgIAAxkBAAIndGJ8GUPH-O61PfHFTUIDYEHWwd3RAAJcuTEbcAboSzzDlR-LOj8yAQADAgADcwADJAQ"
                   )

    await add_item(name='Fly жемчужно-розовый',
                   category_name='Комплект без косточек', category_code='noKost',
                   subcategory_name='Fly', subcategory_code='fly',
                   decription='Комплект с лифом без косточек + трусики бразилиана \n'
                              'Отличный вариант для тех, кто не любит косточки в бюстгальтерах. Лиф fly имеет плотную ленту под чашечкой, что позволяет придерживать даже большой объём груди. \n '
                              'Трусики бразилиана 2х видов:\n'
                              '1. Спереди и сзади кружевной край проходит по ягодицам, ножкам;\n'
                              '2. Спереди классические трусики, а сзади кружной край на ягодицах\n'
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=2500,
                   photo="AgACAgIAAxkBAAIndmJ8Gl3vcihkF0_HnO9gn1zraQo5AAJguTEbcAboS0nKxc-fUS1yAQADAgADcwADJAQ"
                   )


    await add_item(name='Fly  персиковый с цветами',
                   category_name='Комплект без косточек', category_code='noKost',
                   subcategory_name='Fly', subcategory_code='fly',
                   decription='Комплект с лифом без косточек + трусики бразилиана \n'
                              'Отличный вариант для тех, кто не любит косточки в бюстгальтерах. Лиф fly имеет плотную ленту под чашечкой, что позволяет придерживать даже большой объём груди. \n '
                              'Трусики бразилиана 2х видов:\n'
                              '1. Спереди и сзади кружевной край проходит по ягодицам, ножкам;\n'
                              '2. Спереди классические трусики, а сзади кружной край на ягодицах\n'
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=2500,
                   photo="AgACAgIAAxkBAAIneGJ8Goeqopiqj2EXzpNaWuVckHCwAAJhuTEbcAboSxsTyy-z6CB-AQADAgADcwADJAQ"
                   )

    await add_item(name='Fly с удлиненной чашкой',
                   category_name='Комплект без косточек', category_code='noKost',
                   subcategory_name='Fly', subcategory_code='fly',
                   decription='Комплект fly с удлиненной чашечкой без косточек \n'
                              'Комплект выполнен из мягкого кружева-сеточки, которое не чувствуется на теле🙌🏻\n'
                              'В комплекте идут трусики бразилиана, можно заменить на другую модель трусиков \n'
                              '\n'
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=2500,
                   photo="AgACAgIAAxkBAAInemJ8GyftWuPII-OuvsSt3fgAAXsdQAACY7kxG3AG6EsTtHPM7iKMMwEAAwIAA3MAAyQE"
                   )


    await add_item(name='LAVAND',
                   category_name='Комплект без косточек', category_code='noKost',
                   subcategory_name='LAVAND', subcategory_code='lavand',
                   decription='Этот комплект отличается от всех тем, что вы можете сами выбрать чашечку для лифа или трусики:'
                              '• чашка Low — как на фото, с более открытой грудью;'
                              '• чашка Classic — классическая чашечка в виде капельки;'
                              '• трусики стринги или бразилиана🙌🏻'
                              'Комплект выполнен из нежного кружева лавандового цвета💜',
                   price=3000,
                   photo="AgACAgIAAxkBAAInfGJ8HBH-cvaodGj1S4LGC7inndv9AAJkuTEbcAboS4agfpGrhWMaAQADAgADcwADJAQ"
                   )



    await add_item(name='PARADISE персиковый',
                   category_name='Комплект на косточках', category_code='Kost',
                   subcategory_name='PARADISE', subcategory_code='paradise',
                   decription='Шикарный персиковый комплект Paradise выполнен из вышивки на сетке, изделия из этого материала являются более износостойкими чем кружевные\n'
                              '\n'
                              '•чашечки имеют подкладку из сеточки для комфортной носки;\n'
                              '•трусики могут быть стринги или стринги на регуляторах;'
                              '\n'
                              '75A, 80A '
                              '70B, 75B, 80B, 85B \n'
                              '70C, 75C, 80C \n'
                              'XS, S, M, L, XL',
                   price=4590,
                   photo="AgACAgIAAxkBAAIngGJ8HeS03uoV0CAvM_c0FojxZvvgAAJquTEbcAboS9Jl5IykhiVIAQADAgADcwADJAQ"
                   )





    await add_item(name='Classic небесно-голубой',
                   category_name='На косточках', category_code='Kost',
                   subcategory_name='Classic', subcategory_code='calassic',
                   decription=' Классический лиф + трусики стринги'
                              '• Лиф на косточках, подойдет как для большого так и для маленького объема груди, чашка выполнена в виде капельки, что позволяет груди равномерно распределиться в ней\n'
                              '• Трусики стринги\n'
                              '•Сочетание эластичного кружева и мягкой сеточки\n'
                              '70A, 75A, 80A\n'
                              '70B, 75B, 80B, 85B\n'
                              '70C, 75C, 80C, 85C\n'
                              '70D, 75D\n'
                              'XS, S, M, L, XL\n',
                   price=3000,
                   photo="AgACAgIAAxkBAAII7mJUKt4w6IYN3I_fDBkAARr4MaL4_AACA7kxG07FoEokg_1r4ZPytgEAAwIAA3MAAyME"
                   )

    await add_item(name='Classic пыльно-розовый',
                   category_name='На косточках', category_code='Kost',
                   subcategory_name='Classic', subcategory_code='calassic',
                   decription='Классический лиф + трусики стринги\n'
                              '• Лиф на косточках, подойдет как для большого так и для маленького объема груди, чашка выполнена в виде капельки, что позволяет груди равномерно распределиться в ней\nn'
                              '• Трусики стринги\n'
                              '•Сочетание эластичного кружева и мягкой сеточки.\n'
                              '70A, 75A, 80A\n'
                              '70B, 75B, 80B, 85B\n'
                              '70C, 75C, 80C, 85C\n '
                              '70D, 75D\n'
                              'XS, S, M, L, XL',
                   price=3000,
                   photo="AgACAgIAAxkBAAIJE2JULBqiZB3ALnmkmKEBP_MDvc2_AAIGuTEbTsWgSjulFZGE57r2AQADAgADcwADIwQ"
                   )

    await add_item(name='Classic белый',
                   category_name='На косточках', category_code='Kost',
                   subcategory_name='Classic', subcategory_code='calassic',
                   decription='Классический лиф + трусики стринги\n'
                              '• Лиф на косточках, подойдет как для большого так и для маленького объема груди, чашка выполнена в виде капельки, что позволяет груди равномерно распределиться в ней;\n'
                              '• Трусики стринги\n'
                              '•Сочетание эластичного кружева и мягкой сеточки.\n '
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C, 85C\n '
                              '70D, 75D\n '
                              'XS, S, M, L, XL',
                   price=3000,
                   photo="AgACAgIAAxkBAAIJQGJULvD9JV801o4zsc4ZfFfpG07UAAIPuTEbTsWgSquOQeSvQpoyAQADAgADcwADIwQ"
                   )


    await add_item(name='Classic кремовый',
                   category_name='На косточках', category_code='Kost',
                   subcategory_name='Classic', subcategory_code='calassic',
                   decription='Классический лиф + трусики стринги\n'
                              '• Лиф на косточках, подойдет как для большого так и для маленького объема груди, чашка выполнена в виде капельки, что позволяет груди равномерно распределиться в ней;\n'
                              '• Трусики стринги\n'
                              '•Сочетание эластичного кружева и мягкой сеточки.\n '
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C, 85C\n '
                              '70D, 75D\n '
                              'XS, S, M, L, XL',
                   price=3000,
                   photo="AgACAgIAAxkBAAIJS2JULzSG_GFNSR2mJKHU1nVHxkZXAAIQuTEbTsWgSu0-VZbjOo9BAQADAgADcwADIwQ"
                   )

    await add_item(name='Fly пыльно-розовый',
                   category_name='Без косточек', category_code='noKost',
                   subcategory_name='Fly', subcategory_code='fly',
                   decription='Комплект с лифом без косточек + трусики бразилиана \n'
                              'Отличный вариант для тех, кто не любит косточки в бюстгальтерах. Лиф fly имеет плотную ленту под чашечкой, что позволяет придерживать даже большой объём груди. \n '
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=2500,
                   photo="AgACAgIAAxkBAAIJbGJUMA6rbhp7ylzSE6PcppZPYGT1AAITuTEbTsWgSt7Z0_BPEY9QAQADAgADcwADIwQ"
                   )

    await add_item(name='Белый',
                   category_name='Без косточек', category_code='noKost',
                   subcategory_name='Base', subcategory_code='base',
                   decription='Лиф + трусики стринги высокая или средняя посадка\n'
                              'Комплект выполнен из мягкой сеточки, идеально подойдёт для каждодневной носки.\n '
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=990,
                   photo="AgACAgIAAxkBAAILkmJUeeO-IZTRWTxneZLpTuOc1cAXAALhtzEbTsWoSsYOQceDh-IyAQADAgADcwADIwQ"
                   )

    await add_item(name='Чёрный',
                   category_name='Без косточек', category_code='noKost',
                   subcategory_name='Base', subcategory_code='base',
                   decription='Лиф + трусики стринги высокая или средняя посадка\n'
                              'Комплект выполнен из мягкой сеточки, идеально подойдёт для каждодневной носки.\n '
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=990,
                   photo="AgACAgIAAxkBAAIMw2JVhZjmWN1qWOv-1iW1odHdJYvaAAJ4tzEb7W-xStttl8OSkkFZAQADAgADcwADIwQ"
                   )

    await add_item(name='Бежевый',
                   category_name='Без косточек', category_code='noKost',
                   subcategory_name='Base', subcategory_code='base',
                   decription='Лиф + трусики стринги высокая или средняя посадка\n'
                              'Комплект выполнен из мягкой сеточки, идеально подойдёт для каждодневной носки.\n '
                              '70A, 75A, 80A\n '
                              '70B, 75B, 80B, 85B\n '
                              '70C, 75C, 80C\n '
                              'XS, S, M, L, XL',
                   price=990,
                   photo="AgACAgIAAxkBAAIM7WJVhvlNYifvj9bLwbJ6TvzIq28sAAJltzEb7W-xSrPSR1C63eZ1AQADAgADcwADIwQ"
                   )

    await add_item(name='Лиф + средние шорты в чёрном цвете',
                   category_name='Без косточек', category_code='noKost',
                   subcategory_name='Basic', subcategory_code='basic',
                   decription='Базовый комплект из хлопка\n '
                              'Доступен в 4х цветах \n '
                              'Чёрный/белый/голубой/лавандовый\n '
                              'Может служить не только как нижнее белье, но и как одежда для дома/спорта',
                   price=3000,
                   photo="AgACAgIAAxkBAAIM7WJVhvlNYifvj9bLwbJ6TvzIq28sAAJltzEb7W-xSrPSR1C63eZ1AQADAgADcwADIwQ"
                   )

    await add_item(name='Топ + высокие шортики в голубом цвете',
                   category_name='Без косточек', category_code='noKost',
                   subcategory_name='Basic', subcategory_code='basic',
                   decription='Базовый комплект из хлопка\n '
                              'Доступен в 4х цветах \n '
                              'Чёрный/белый/голубой/лавандовый\n '
                              'Может служить не только как нижнее белье, но и как одежда для дома/спорта',
                   price=2500,
                   photo="AgACAgIAAxkBAAINBWJViEUSy68omVmfCxiD-5EgjpJvAAKFtzEb7W-xSv9Kh4Q86eLYAQADAgADcwADIwQ"
                   )

    await add_item(name='Лиф + высокие стринги в белом цвете',
                   category_name='Без косточек', category_code='noKost',
                   subcategory_name='Basic', subcategory_code='basic',
                   decription='Базовый комплект из хлопка\n '
                              'Доступен в 4х цветах \n '
                              'Чёрный/белый/голубой/лавандовый\n '
                              'Может служить не только как нижнее белье, но и как одежда для дома/спорта',
                   price=3000,
                   photo="AgACAgIAAxkBAAINEWJViJDZc9fzpVN9t-LOgNfLm28IAAKHtzEb7W-xSnXdn1IYuFSlAQADAgADcwADIwQ"
                   )

    await add_item(name='Топ + средние стринги в лавандовом цвете',
                   category_name='Без косточек', category_code='noKost',
                   subcategory_name='Basic', subcategory_code='basic',
                   decription='Базовый комплект из хлопка\n '
                              'Доступен в 4х цветах \n '
                              'Чёрный/белый/голубой/лавандовый\n '
                              'Может служить не только как нижнее белье, но и как одежда для дома/спорта',
                   price=2500,
                   photo="AgACAgIAAxkBAAINHWJViMI5oCRbxazAeO7UdE1Gfan4AAKJtzEb7W-xSriyJBHiTIogAQADAgADcwADIwQ"
                   )

"""

asyncio.get_event_loop().run_until_complete(add_items())

