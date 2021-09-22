from pyrogram import Client, filters
from plugins.menu import keyboards
import utils
import db


@Client.on_message(filters.regex(pattern='^.*меню.*$') & filters.private & utils.check_user)
async def menu(_, message):
    """
    Функция которая срабатывает когда пользователь хочет перейти в режим работы с меню
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: сообщение
    :return:
    """
    utils.update_username_in_db_if_not_matches(message.from_user.id, message.from_user.username)
    
    text = f"Ты вышел в главное меню.\n" \
           f"Выбери, что будем делать дальше на клавиатуре внизу экрана"
    db.set_task_type(message.from_user.id, 'menu')
    await message.reply_text(text, reply_markup=keyboards.menu_keyboard)


@Client.on_message(filters.command('keyboard') & filters.private & utils.check_user &
                   utils.task_type_filter('menu'))
async def keyboard(_, message):
    """
    Возвращает юзеру клавиатуру
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: сообщение
    :return:
    """
    await message.reply_text('Воть ^-^', reply_markup=keyboards.menu_keyboard)
