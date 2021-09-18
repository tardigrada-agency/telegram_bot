import pyrogram.types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton
import requests
from plugins.jinja2png import jinja2png_utils
import os

menu = ['выбрать', 'меню']
menu_keyboard = ReplyKeyboardMarkup([
    *([KeyboardButton(k)] for k in menu)
])
if 'JINJA2PNG_HOST' in os.environ.keys():
    url = f"http://{os.environ['JINJA2PNG_HOST']}:{os.environ['JINJA2PNG_PORT']}/template/list"


def get_template_list_keyboard() -> pyrogram.types.InlineKeyboardMarkup:
    response = requests.request("GET", url).json()
    templates_keyboard = InlineKeyboardMarkup([
        *([InlineKeyboardButton(k, callback_data=f'set_template={k}')] for k in jinja2png_utils.get_template_list())
    ])
    return templates_keyboard

