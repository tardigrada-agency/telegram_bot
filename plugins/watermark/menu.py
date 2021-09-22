from plugins.watermark import watermark_db
from plugins.watermark import keyboards
from pyrogram import Client, filters
from plugins.watermark import modes
import utils
import db


@Client.on_message(filters.regex(pattern='^.*ватермарка.*$') & filters.private & utils.check_user)
async def menu(_, message):
    """
    Функция которая срабатывает когда пользователь хочет перейти в режим работы с ватермаркой
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: сообщение
    :return:
    """
    utils.update_username_in_db_if_not_matches(message.from_user.id, message.from_user.username)

    if not watermark_db.check_user(message.from_user.id):
        watermark_db.add_user(message.from_user.id, modes.default['color'],
                              modes.default['type'], modes.default['mode'],
                              modes.default['size'])
    text = f"Ты вошел в режим добавления ватермарки.\n" \
           f"Внизу экрана у тебя есть клавиатура настройки ватермарки.\n" \
           f"Для добавление ватермарки пришли фотографию, видео, файл, zip архив"
    db.set_task_type(message.from_user.id, 'watermark')
    await message.reply_text(text, reply_markup=keyboards.watermark_menu_keyboard)


@Client.on_message(filters.command('keyboard') & filters.private & utils.check_user &
                   utils.task_type_filter('watermark'))
async def watermark_keyboard(_, message):
    await message.reply_text('Воть ^-^', reply_markup=keyboards.watermark_menu_keyboard)
