from collections import defaultdict
from copy import deepcopy
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
    LabeledPrice,
)
from aiogram.dispatcher.filters import Text

from create_bot import bot
from constants import PAYMENT_TOKEN
from user import User
from handlers.general import reload_reply_markup

from data_base.sqlite_db import sql_get_menu


navigation_markup = InlineKeyboardMarkup()
back_scroll_btn = InlineKeyboardButton(
    '⬅️', callback_data='get_previous_menu_item'
)
forward_scroll_btn = InlineKeyboardButton(
    '➡️', callback_data='get_next_menu_item'
)
navigation_markup.add(back_scroll_btn, forward_scroll_btn)

admin_buttons = []

users_dict = defaultdict(User)  # Structure: { chat_id: User }
delete_from_basket_btn = InlineKeyboardButton(
    '🔻', callback_data='delete_one_item_from_basket'
)
add_to_basket_btn = InlineKeyboardButton(
    '🔺', callback_data='add_one_item_to_basket'
)
# counter_of_item_btn = InlineKeyboardButton('',
# callback_data='show_this_type_of_items_in_basket')
pay_btn = InlineKeyboardButton('Pay order 💳', callback_data='pay')


async def return_markup_with_relevant_item_counter(
    chat_id: int, menu_item: tuple
) -> InlineKeyboardMarkup:
    new_markup = deepcopy(navigation_markup)
    item_counter = 0

    if menu_item in users_dict[chat_id].cart:
        item_counter = users_dict[chat_id].cart[menu_item]
    counter_btn = InlineKeyboardButton(
        item_counter, callback_data='show_this_type_of_items_in_basket'
    )

    new_markup.add(delete_from_basket_btn, counter_btn, add_to_basket_btn)
    new_markup.add(pay_btn)

    return new_markup


async def scroll_menu_item_forward_or_back(
    callback: types.CallbackQuery,
) -> None:
    menu: list = await sql_get_menu()

    index_of_item_in_view = users_dict[
        callback.message.chat.id
    ].index_of_current_item_in_view
    if callback.data == 'get_previous_menu_item':
        if index_of_item_in_view == 0:
            index_of_item_in_view = len(menu) - 1
        else:
            index_of_item_in_view -= 1
    elif callback.data == 'get_next_menu_item':
        if index_of_item_in_view == len(menu) - 1:
            index_of_item_in_view = 0
        else:
            index_of_item_in_view += 1

    users_dict[
        callback.message.chat.id
    ].index_of_current_item_in_view = index_of_item_in_view

    tmp_markup = await return_markup_with_relevant_item_counter(
        callback.message.chat.id, menu[index_of_item_in_view]
    )

    menu_item = menu[index_of_item_in_view]
    new_photo = InputMediaPhoto(media=menu_item[0])

    await callback.message.edit_media(new_photo)
    # ToDo: make format change in one place
    await callback.message.edit_caption(
        f"<b><i>{menu_item[1]}</i></b>\n"
        f"<i>Description</i>: {menu_item[2]}\n"
        f"<i>Price</i>: {menu_item[3]} $",
        parse_mode="html",
        reply_markup=tmp_markup,
    )

    await callback.answer()


# send menu item to user
async def send_menu_item_to_user(
    message: types.Message, menu_item: tuple
) -> None:
    if message.chat.id not in users_dict:
        users_dict[message.chat.id] = User(
            message.from_user.id, message.from_user.username
        )

    tmp_markup = await return_markup_with_relevant_item_counter(
        message.chat.id, menu_item
    )
    await bot.send_photo(
        message.from_user.id,
        menu_item[0],
        f"<b><i>{menu_item[1]}</i></b>\n"
        f"<i>Description</i>: {menu_item[2]}\n"
        f"<i>Price</i>: {menu_item[3]} $",
        parse_mode="html",
        reply_markup=tmp_markup,
    )


async def delete_one_item_from_basket(callback: types.CallbackQuery) -> None:
    chat_id = callback.message.chat.id
    menu: list = await sql_get_menu()
    menu_item = menu[users_dict[chat_id].index_of_current_item_in_view]

    if menu_item in users_dict[chat_id].cart:
        if users_dict[chat_id].cart[menu_item] == 1:
            del users_dict[chat_id].cart[menu_item]
        else:
            users_dict[chat_id].cart[menu_item] -= 1

        tmp_markup = await return_markup_with_relevant_item_counter(
            chat_id, menu_item
        )
        await reload_reply_markup(callback, tmp_markup)

    await callback.answer()


async def add_one_item_to_basket(callback: types.CallbackQuery) -> None:
    chat_id = callback.message.chat.id
    menu: list = await sql_get_menu()
    menu_item = menu[users_dict[chat_id].index_of_current_item_in_view]

    if menu_item not in users_dict[chat_id].cart:
        users_dict[chat_id].cart[menu_item] = 0
    users_dict[chat_id].cart[menu_item] += 1

    tmp_markup = await return_markup_with_relevant_item_counter(
        chat_id, menu_item
    )
    await reload_reply_markup(callback, tmp_markup)

    await callback.answer()


async def show_alert_with_count_of_items(
    callback: types.CallbackQuery,
) -> None:
    chat_id = callback.message.chat.id
    menu: list = await sql_get_menu()
    menu_item = menu[users_dict[chat_id].index_of_current_item_in_view]

    counter_of_item = 0
    if menu_item in users_dict[chat_id].cart:
        counter_of_item = users_dict[chat_id].cart[menu_item]

    additional_s = 's'
    if counter_of_item == 1:
        additional_s = ''

    await callback.answer(
        f"You've chosen {counter_of_item} {menu_item[1]}" + additional_s,
        show_alert=True,
    )


async def pay_order(callback: types.CallbackQuery) -> None:
    chat_id = callback.message.chat.id
    if not users_dict[chat_id].cart:
        await callback.answer("Your basket is empty!", show_alert=True)
        return

    order = []
    for menu_item, count_of_item in users_dict[chat_id].cart.items():
        order.append(
            LabeledPrice(
                label=f"{menu_item[1]} x {count_of_item}",
                amount=int(menu_item[3] * count_of_item * 100),
            )
        )

    current_datetime = datetime.now()
    current_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    await bot.send_invoice(
        callback.message.chat.id,
        title='Your order',
        description=current_datetime,
        payload='invoice',
        provider_token=PAYMENT_TOKEN,
        currency='USD',
        prices=order,
    )

    await callback.answer()


async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery) -> None:
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


async def successful_payment(message: types.Message) -> None:
    chat_id = message.chat.id
    users_dict[chat_id].cart.clear()

    # payment_info = message.successful_payment.to_python()
    # { 'currency', 'total_amount', 'invoice_payload',
    # 'telegram_payment_charge_id', 'provider_payment_charge_id' }
    await message.answer("Your order is starting to be prepared:)")
    # ToDo: write order in db with all orders...


def register_handlers_general(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        scroll_menu_item_forward_or_back, Text(startswith='get_')
    )

    dp.register_callback_query_handler(
        delete_one_item_from_basket, text=delete_from_basket_btn.callback_data
    )
    dp.register_callback_query_handler(
        add_one_item_to_basket, text=add_to_basket_btn.callback_data
    )
    dp.register_callback_query_handler(
        show_alert_with_count_of_items,
        text='show_this_type_of_items_in_basket',
    )

    # payment handlers
    dp.register_callback_query_handler(pay_order, text=pay_btn.callback_data)
    dp.register_pre_checkout_query_handler(
        pre_checkout_query, lambda query: True
    )
    dp.register_message_handler(
        successful_payment, content_types=types.ContentType.SUCCESSFUL_PAYMENT
    )
