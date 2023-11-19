from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

BOT_LINK = 'https://t.me/PizzaSlice_bot'
BOT_TOKEN = os.getenv('BOT_TOKEN')
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')
