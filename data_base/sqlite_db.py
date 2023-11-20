import sqlite3 as sq

from aiogram.dispatcher import FSMContext

from typing import List


# connecting to db (or creating new db table if it's not exist)
def sql_start() -> None:
    """Create or connect to DB with menu"""
    global base, cur
    base = sq.connect('pizza_bot.db')
    cur = base.cursor()

    if base:
        print('Data base connected OK')

    base.execute(
        "CREATE TABLE IF NOT EXISTS menu(img TEXT, name "
        "TEXT PRIMARY KEY, description TEXT, price FLOAT)"
    )
    base.commit()


# add menu item to db
async def sql_add_item(state: FSMContext) -> None:
    """Add item to pizzeria menu"""
    async with state.proxy() as data:
        cur.execute(
            "INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values())
        )
        base.commit()


# return list with menu
async def sql_get_menu() -> List[List[str]]:
    """Return List with pizzeria menu"""
    return cur.execute("SELECT * FROM menu").fetchall()


async def sql_delete_menu_item(item: List[str]) -> None:
    """Delete item in pizzeria menu"""
    cur.execute(f"DELETE FROM menu WHERE img={item[0]} AND name=\"{item[1]}\"")
    base.commit()
