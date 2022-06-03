from pyrogram import Client, filters
from plugins.menu import keyboards
import utils
import db


@Client.on_message(filters.command(commands=['start', 'help']) & filters.private)
async def send_welcome(_, message):
    """
    Функция которая срабатывает когда пользователь прислал /start (запустил бота) или /help
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message:
    :return:
    """

    text_new = f"Привет!\n" \
               f"Я бот mediathings созданный для @sotaproject, @antresol_avia и @tardigrada_agency\n" \
               f"Твой ID: `{message.from_user.id}`\n" \
               f"Скажи свой ID админу, чтобы он тебя добавил.\n"
    text_old = f"Привет!\n" \
               f"Я бот mediathings созданный для @sotaproject, @antresol_avia и @tardigrada_agency\n" \
               f"Твой ID: `{message.from_user.id}`\n" \
               f"Ты уже в базе, поэтому вот тебе клавиатура :)"
    if db.check_user_in_users(message.from_user.id):
        utils.update_username_in_db_if_not_matches(message.from_user.id, message.from_user.username)

        await message.reply_text(text_old, reply_markup=keyboards.menu_keyboard)
    else:
        await message.reply_text(text_new)


@Client.on_message(~utils.check_user & filters.private)
async def no_access(_, message):
    """
    Если у пользователя нет доступа для работы с ботом - сообщим ему об этом
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message:
    :return:
    """
    await message.reply(f"У тебя нет доступа :(\n"
                        f"Твой ID: `{message.chat.id}`\n"
                        f"Попробуй попросить админа, чтобы тебя добавили!")
