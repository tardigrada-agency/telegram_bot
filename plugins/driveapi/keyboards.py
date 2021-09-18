from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton

menu = ['меню']
menu_keyboard = ReplyKeyboardMarkup([
    *([KeyboardButton(k)] for k in menu)
])
