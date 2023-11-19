from aiogram.utils import executor

from create_bot import dp
from data_base import sqlite_db
from handlers import cart, client, general

# from menu_commands import add_commands_to_bot_menu


async def on_startup(_) -> None:
    print('Bot is online now!')
    sqlite_db.sql_start()
    # result = await add_commands_to_bot_menu()


if __name__ == "__main__":
    # admin.register_handlers_admin(dp)
    cart.register_handlers_general(dp)
    client.register_handlers_client(dp)
    general.register_handlers_general(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
