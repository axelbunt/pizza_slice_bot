# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
#
# from aiogram import types, Dispatcher
# from aiogram.dispatcher.filters import Text
#
# from create_bot import bot
# from data_base.sqlite_db import sql_add_item, sql_get_menu, sql_delete_menu_item
# from handlers.general import send_menu_item_to_user, index_of_current_item
#
# from aiogram.types import InlineKeyboardButton
#
#
# ADMIN_ID = None  # id of current moderator
#
# edit_item_btn = InlineKeyboardButton('Edit item ✍️', callback_data='edit_item')
# add_item_btn = InlineKeyboardButton('Add new item ✅', callback_data='add_item')
# delete_item_btn = InlineKeyboardButton('Delete item ❌', callback_data='delete_item')
#
#
# # class with states
# class FSMAdmin(StatesGroup):
#     # order of states are next...
#     awaiting_photo = State()
#     awaiting_name = State()
#     awaiting_description = State()
#     awaiting_price = State()
#
#
# # get ID of new moderator
# async def get_new_moderator_id(message: types.Message) -> None:
#     global ADMIN_ID
#     ADMIN_ID = message.from_user.id
#     await bot.send_message(message.from_user.id, 'Hello, Admin:)')
#
#     menu: list = await sql_get_menu()
#     await send_menu_item_to_user(message, menu[0], [[edit_item_btn, delete_item_btn], add_item_btn])
#
#     await message.delete()
#
#
# # starting uploading new menu item
# async def start_new_item_uploading(callback: types.CallbackQuery) -> None:
#     if callback.from_user.id == ADMIN_ID:  # check if current user is moderator, then proceed fsm
#         await FSMAdmin.awaiting_photo.set()
#         await bot.send_message(callback.message.chat.id, 'Upload photo:')
#         await callback.answer()
#
#
# # handling item photo and saving it to memory
# async def load_photo(message: types.Message, state: FSMContext) -> None:
#     async with state.proxy() as data:
#         data['photo'] = message.photo[0].file_id  # we're saving not all photo, but it's ID
#     await FSMAdmin.next()  # change fsm state
#     await message.reply('Now enter item name:')
#
#
# # handling item name
# async def load_name(message: types.Message, state: FSMContext) -> None:
#     async with state.proxy() as data:
#         data['name'] = message.text
#     await FSMAdmin.next()
#     await message.reply('Now enter item description:')
#
#
# # handling item description
# async def load_description(message: types.Message, state: FSMContext) -> None:
#     async with state.proxy() as data:
#         data['description'] = message.text
#     await FSMAdmin.next()
#     await message.reply('Now enter item price:')
#
#
# # handling item price and finishing FSM
# async def load_price(message: types.Message, state: FSMContext) -> None:
#     async with state.proxy() as data:
#         data['price'] = float(message.text)
#
#     # async with state.proxy() as data:
#     #     await message.reply(str(data))
#     await sql_add_item(state)
#
#     await state.finish()  # this command cleans data and end FSM
#     await message.answer('Now all done')
#
#
# # exit state
# async def cancel_handler(message: types.Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply('Ok...')
#
#
# async def delete_menu_item(callback: types.CallbackQuery) -> None:
#     if callback.from_user.id == ADMIN_ID:
#         menu = await sql_get_menu()
#         item = menu[index_of_current_item]
#         await sql_delete_menu_item(item)
#
#         await callback.answer()
#
#
# # register admin handlers
# def register_handlers_admin(dp: Dispatcher) -> None:
#     # start FSM
#     dp.register_callback_query_handler(start_new_item_uploading, text='add_item', state=None)
#
#     # handle `cancel` command
#     dp.register_message_handler(cancel_handler, state='*', commands=['cancel'])
#     dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
#
#     # FSM states
#     dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.awaiting_photo)
#     dp.register_message_handler(load_name, state=FSMAdmin.awaiting_name)
#     dp.register_message_handler(load_description, state=FSMAdmin.awaiting_description)
#     dp.register_message_handler(load_price, state=FSMAdmin.awaiting_price)
#
#     # get new moderator id, check if current user is admin in group
#     dp.register_message_handler(get_new_moderator_id, commands=['moderator'], is_chat_admin=True)
#
#     # delete menu item
#     dp.register_callback_query_handler(delete_menu_item, text='delete_item')
