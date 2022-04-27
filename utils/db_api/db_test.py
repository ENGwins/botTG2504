import asyncio

from data import config
from utils.db_api import quick_commands as command
from utils.db_api.db_gino import db


async def db_test():
    await db.set_bind(config.POSTGRES_URI)
#    await db.gino.drop_all()
#    await db.gino.create_all()

    #    await quick_commands.add_user(1,'Sergo','','432','ban')
#    await command.add_user(1, 'ddsc', 'ddd', 'dasd')
#    await command.add_user(2, 'dds2c', 'd2dd', 'd2asd')

    users = await command.select_all_users()
    print(users)

    count = await command.count_users()
    print(count)

    user = await command.select_user(1)
    print(user)


loop=asyncio.get_event_loop()
loop.run_until_complete(db_test())

"""if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db_test())
"""