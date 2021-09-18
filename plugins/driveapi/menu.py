from pyrogram import Client, filters
from plugins.driveapi import keyboards
import utils
import db


@Client.on_message(filters.regex(pattern='^.*поиск.*$') & filters.private & utils.check_user)
async def search(_, message):
    """
    Функция которая срабатывает когда пользователь хочет перейти в режим поиска фотографий
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: сообщение
    :return:
    """
    text = f"Ты вошел в режим поиска фотографий.\n" \
           f"Пришли мне запрос, я пришлю тебе фотографии"
    db.set_task_type(message.from_user.id, 'driveapi')
    await message.reply_text(text, reply_markup=keyboards.menu_keyboard)
