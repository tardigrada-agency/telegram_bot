from pyrogram.types import ReplyKeyboardRemove
from plugins.watermark import watermark_db
from plugins.jinja2png import jinja2png_db
from pyrogram import Client, filters
from plugins.menu import keyboards
import utils
import time
import db


temp_users = {}


@Client.on_message(filters.command('whoami') & filters.private & utils.check_user &
                   utils.task_type_filter('menu'))
async def whoami(_, message):
    """
    Возвращает юзеру информацию о нем
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: сообщение
    :return:
    """
    user = db.get_user(message.from_user.id)
    print(type(user[5]))
    await message.reply_text(f"```"
                             f"Твой ид:        {user[0]}\n"
                             f"Твой username:  {user[1]}\n"
                             f"Твое имя:       {user[2]}\n"
                             f"Твоя должность: {user[3]}\n"
                             f"Ты админ:       {'да' if user[4] else 'нет'}\n"
                             f"Добавлен:       {user[5]}"
                             f"```", parse_mode="markdown")


@Client.on_message(filters.command('users') & filters.private & utils.check_user &
                   utils.task_type_filter('menu') & utils.user_is_admin)
async def users(_, message):
    """
    Возвращает список юзеров, доступно только админам
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: сообщение
    """
    users_from_db = db.get_users()
    text = '```' \
           f'+{"—"* 113}+'
    text += '\n' \
            f'| id {" "*7} ' \
            f'| username {" "*11} ' \
            f'| name {" "*15} ' \
            f'| position {" "*3} ' \
            f'| is_admin ' \
            f'| date {" "*21} ' \
            f'|'
    text += f'\n+{"—"* 113}+'
    for u in users_from_db:
        text += f"\n" \
                f"| {str(u[0])+' '*(10-len(str(u[0])))} " \
                f"| {u[1]+' '*(20-len(str(u[1])))} " \
                f"| {u[2]+' '*(20-len(str(u[2])))} " \
                f"| {u[3]+' '*(12-len(str(u[3])))} " \
                f"| {'да ' if u[4] else 'нет'}      " \
                f"| {u[5]} |\n"

        text += f'+{"—"* 113}+'
    text += '```'
    await message.reply_text(text, parse_mode="markdown")


@Client.on_message(filters.command('useradd') & filters.private & utils.check_user &
                   utils.task_type_filter('menu') & utils.user_is_admin)
async def useradd(client, message):
    """
    Команда добавления нового пользователя в базу
    :param client: Клиент для работы с телеграмом
    :param message: сообщение
    """
    started = time.strftime('%Y-%m-%d %H:%M:%S')
    command_info = "Нужно заполнить 5 полей: ID, username, Имя Фамилия, Должность, Сделать админом (Да/Нет). \n\n" \
                   "Данные для каждого поля нужно писать с **новой** строки. " \
                   "Если вы хотите оставить поле пустым, то пропустити одну строку. \n\n" \
                   "Пример использования:\n```" \
                   "/useradd\n" \
                   "123456789\n" \
                   "username\n" \
                   "Имя Фамилия\n" \
                   "Должность\n" \
                   "Нет```"
    lines = message.text.split('\n')
    if len(lines) != 6:
        await message.reply_text(command_info)
        return
    del lines[0]
    user = utils.User(int(lines[0]), str(lines[1]), str(lines[2]), str(lines[3]))

    if lines[4].lower() == 'да':
        user.is_admin = True

    user.add_to_db()

    await message.reply_text(f"{user.name} успешно добавлен!")
    try:
        await client.send_message(
                chat_id=user.telegram_id,
                text=f'Тебя добавили!!!\n'
                     f'Теперь ты можешь использовать функции бота.\n'
                     f'{"Ты админ" if user.is_admin else ""}',
                reply_markup=keyboards.menu_keyboard
        )

    except:
        pass
    ended = time.strftime('%Y-%m-%d %H:%M:%S')
    db.add_activity(message.from_user.id, 'menu', 'useradd',
                    f'telegram_id={user.telegram_id}', started, ended)


@Client.on_message(filters.command('userdel') & filters.private & utils.check_user &
                   utils.task_type_filter('menu') & utils.user_is_admin)
async def userdel(client, message):
    """
    Команда удаления пользователя из базы
    :param client: Клиент для работы с телеграмом
    :param message: сообщение
    """
    if len(message.text.split(' ')) != 2:
        await message.reply_text('Сообщение должно быть в формате `/userdel 123456789`', parse_mode="markdown")
        return
    user_id = int(message.text.split(' ')[1])
    if not db.check_user_in_users(user_id):
        await message.reply_text(f'Пользователя `{user_id} нету в базу :(`', parse_mode="markdown")
        return
    db.delete_user(user_id)
    if watermark_db.check_user(user_id):
        watermark_db.delete_user(user_id)
    if jinja2png_db.check_user(user_id):
        jinja2png_db.delete_user(user_id)
    await client.send_message(
                chat_id=user_id,
                text='Тебя удалили из базы, тебе больше не доступны функции бота.',
                reply_markup=ReplyKeyboardRemove(),
          )
    await message.reply_text(f'`{user_id}` удален из базы.')
