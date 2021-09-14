from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton

menu = ['ватермарка', 'шаблоны', 'поиск фото']
menu_keyboard = ReplyKeyboardMarkup([
    *([KeyboardButton(k)] for k in menu)
])
