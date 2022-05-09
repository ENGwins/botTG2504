import asyncio

from utils.db_api.db_commands import add_item


async def add_items():
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



asyncio.get_event_loop().run_until_complete(add_items())

