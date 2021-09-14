from plugins.jinja2png import jinja2png_utils
from plugins.jinja2png import jinja2png_db
from plugins.jinja2png import keyboards
from pyrogram import Client, filters
import utils
import db


@Client.on_message(filters.regex(pattern='^.*шаблоны.*$') & filters.private & utils.check_user)
async def menu(_, message):
    """
    Функция которая срабатывает когда пользователь хочет перейти в режим работы с шаблонами
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: сообщение
    :return:
    """
    template_list = jinja2png_utils.get_template_list()
    if len(template_list) >= 1:
        if not jinja2png_db.check_user(message.from_user.id):
            jinja2png_db.add_user(message.from_user.id, jinja2png_utils.get_template_list()[0])
        text = f"Ты вошел в режим работы с шаблонами.\n" \
               f"Внизу экрана ты можешь выбрать шаблон.\n" \
               f"Чтобы использовать шаблон прешли текст и картинку"
        db.set_task_type(message.from_user.id, 'jinja2png')
        await message.reply_text(text, reply_markup=keyboards.menu_keyboard)
    else:
        await message.reply_text('Не найдено не одного шаблона, не возможно перейти в режим шаблонизации')


@Client.on_message(filters.regex(pattern='^.*выбрать.*$') & filters.private & utils.check_user &
                   utils.task_type_filter('jinja2png'))
async def select_template(_, message):
    """
    Функция выдает клавиатуру выбора шаблона
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: сообщение
    :return:
    """
    text = f"Выбери шаблон:"
    await message.reply_text(text, reply_markup=keyboards.get_template_list_keyboard())


@Client.on_callback_query(jinja2png_utils.set_template & utils.check_user
                          & utils.task_type_filter(type_name='jinja2png'))
async def set_template_callback(client, query):
    """
    Принимает callback от нажатия кнопок в keyboards.get_template_list_keyboard()
    :param client: Клиент для работы с телеграмом
    :param query: действие пользователя которое запустило эту функцию
    :return:
    """
    jinja2png_db.set_jinja2png_setting(query.from_user.id, query.data.split('=')[1])
    await client.answer_callback_query(query.id, text=f'шаблон установлен!')


@Client.on_message(filters.command('keyboard') & filters.private & utils.check_user &
                   utils.task_type_filter('jinja2png'))
async def keyboard(_, message):
    await message.reply_text('Воть ^-^', reply_markup=keyboards.menu_keyboard)
