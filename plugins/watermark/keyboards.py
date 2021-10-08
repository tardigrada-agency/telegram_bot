from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton
from plugins.watermark import modes
# Клавиатура для выбора цвета логотипа
colors = {'🔴': 'red', '⚫': 'black', '⚪': 'white', '🟢': 'green'}
color_keyboard = InlineKeyboardMarkup([[
    *(InlineKeyboardButton(k, callback_data=f'new_color={v}') for k, v in colors.items())
]])

# Клавиатура для выбора размера логотипа
sizes = {'small': 1, 'middle': 2, 'big': 3}
size_keyboard = InlineKeyboardMarkup([[
    *(InlineKeyboardButton(k, callback_data=f'new_size={v}') for k, v in sizes.items())
]])

# Клавиатура для выбора типа логотипа
types = {'русский': 'rus', 'английский': 'eng'}
type_keyboard = InlineKeyboardMarkup([[
    *(InlineKeyboardButton(k, callback_data=f'new_type={v}') for k, v in types.items())
]])

# Создания клавиатуры выбора режима работы
modes_keyboard = InlineKeyboardMarkup([[
    *(InlineKeyboardButton(v["button_text"], callback_data=f'new_mode={k}') for k, v in modes.modes.items())
]])

# Главное меню
watermark_menu = ('цвет', 'размер', 'режим', 'тип', 'меню')
watermark_menu_keyboard = ReplyKeyboardMarkup([
    *([KeyboardButton(i)] for i in watermark_menu)
])

