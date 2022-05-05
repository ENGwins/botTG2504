from utils.db_api.db_commands import add_item

await add_item(name='Asus',
               category_name='Электроника',category_code='Electric',
               subcategory_name='Компы',subcategory_code='PCs',
               price=100,photo='-'
               )
await add_item(name='Dell',
               category_name='Электроника',category_code='Electric',
               subcategory_name='Компы',subcategory_code='PCs',
               price=100,photo='-'
               )
await add_item(name='Apple',
               category_name='Электроника',category_code='Electric',
               subcategory_name='Компы',subcategory_code='PCs',
               price=100,photo='-'
               )
await add_item(name='PewDiePie',
               category_name='Услуги рекламы',category_code='Ads',
               subcategory_name='На ютуб',subcategory_code='YouTube',
               price=100,photo='-'
               )
await add_item(name='Орленок',
               category_name='Услуги рекламы',category_code='Ads',
               subcategory_name='Вконтакте',subcategory_code='VK',
               price=100,photo='-'
               )
