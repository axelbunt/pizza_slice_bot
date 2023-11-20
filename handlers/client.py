from aiogram import types, Dispatcher
from create_bot import bot

from handlers.general import send_message_directly
from handlers.cart import send_menu_item_to_user

from data_base.sqlite_db import sql_get_menu
import menu_commands


async def start(message: types.Message) -> None:
    await send_message_directly(message, "Hi! I'm waiting for your orders:)")


async def send_list_of_commands_to_user(message: types.Message) -> None:
    help_message = "Use:\n"
    for command in menu_commands.COMMANDS:
        help_message += '/' + command.command + " – to " + \
         command.description + '\n'
    await send_message_directly(message, help_message)


async def send_pizzeria_hours(message: types.Message) -> None:
    await send_message_directly(
        message,
        "We're working on:\n"
        "Mon-Fri from 9:00 to 22:00,\n"
        "Sut-Sun from 10:00 to 20:00",
    )


async def send_pizzeria_location(message: types.Message) -> None:
    await send_message_directly(message, "You can find us at this address:")
    # ToDo: addresses in db, calculation of nearest pizzeria
    await bot.send_location(
        message.from_user.id,
        latitude=41.8954072,
        longitude=12.477454,
        horizontal_accuracy=500,
    )


async def send_pizzeria_menu(message: types.Message) -> None:
    menu: list = await sql_get_menu()

    await send_menu_item_to_user(message, menu[0])


# register bot commands
def register_handlers_client(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(
        send_list_of_commands_to_user,
        commands=[menu_commands.HelpBotCommand().command],
    )

    dp.register_message_handler(
        send_pizzeria_hours,
        commands=[menu_commands.HoursBotCommand().command],
    )
    dp.register_message_handler(
        send_pizzeria_location,
        commands=[menu_commands.LocationBotCommand().command],
    )
    dp.register_message_handler(
        send_pizzeria_menu,
        commands=[menu_commands.MenuBotCommand().command],
    )
