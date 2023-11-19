import json
import string

from aiogram import types, Dispatcher, exceptions
from aiogram.types import InlineKeyboardMarkup

from create_bot import bot
from constants import BOT_LINK


async def reload_reply_markup(callback: types.CallbackQuery,
                              new_markup: InlineKeyboardMarkup) -> None:
    """update bot message markup"""
    await callback.message.edit_reply_markup(reply_markup=new_markup)


async def send_message_directly(message: types.Message, message_to_user: str,
                                reply_markup=None) -> None:
    """safe function to send a message to users directly"""
    try:
        await bot.send_message(message.from_user.id, message_to_user,
                               reply_markup=reply_markup)
    # if a user hasn't sent a message to bot yet
    except exceptions.Unauthorized:
        await message.delete()
        await message.reply(f'Chat with bot directly first: \n{BOT_LINK}')


async def delete_obscene_messages(message: types.Message) -> None:
    # get a set of words from a user message and delete all masking 
    # symbols (for example: ,.!)
    message_to_check = {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
                        message.text.split(' ')}
    obscene_messages = set(json.load(open('censorship/censorship.json')))
    if message_to_check.intersection(obscene_messages) != set():
        await message.reply('Obscene messages is forbidden')
        await message.delete()


def register_handlers_general(dp: Dispatcher) -> None:
    dp.register_message_handler(delete_obscene_messages)
