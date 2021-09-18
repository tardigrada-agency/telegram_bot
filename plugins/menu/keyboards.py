from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton
import os
menu = []
if 'WATERMARK_HOST' in os.environ.keys():
    menu.append('ватермарка')
if 'JINJA2PNG_HOST' in os.environ.keys():
    menu.append('шаблоны')
if 'DRIVEAPI_HOST' in os.environ.keys():
    menu.append('поиск')

menu_keyboard = ReplyKeyboardMarkup([
    *([KeyboardButton(k)] for k in menu)
])
