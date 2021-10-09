from plugins.watermark import watermark_utils
from plugins.watermark import watermark_db
from plugins.watermark import keyboards
from pyrogram import Client, filters
import utils


@Client.on_message(filters.regex(pattern=r'^.*тип.*$') & filters.private & utils.check_user
                   & utils.task_type_filter(type_name='watermark'))
async def type_select(_, message):
    """
    Присылает клавиатуру выбора языка логотипа
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    await message.reply('Выбери тип:', reply_markup=keyboards.type_keyboard)


@Client.on_callback_query(watermark_utils.new_type & utils.check_user
                          & utils.task_type_filter(type_name='watermark'))
async def type_callback(client, query):
    """
    Принимает callback от нажатия кнопок в keyboards.type_keyboard
    :param client: Клиент для работы с телеграмом
    :param query: действие пользователя которое запустило эту функцию
    :return:
    """
    watermark_db.set_setting(query.from_user.id, 'type', query.data.split('=')[1])
    await client.answer_callback_query(query.id, text=f'Тип установлен!')


@Client.on_message(filters.regex(pattern='^.*цвет.*$') & filters.private & utils.check_user
                   & utils.task_type_filter(type_name='watermark'))
async def color_select(_, message):
    """
    Присылает клавиатуру выбора размера логотипа
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    await message.reply('Выбери цвет:', reply_markup=keyboards.color_keyboard)


@Client.on_callback_query(watermark_utils.new_color & utils.check_user
                          & utils.task_type_filter(type_name='watermark'))
async def color_callback(client, query):
    """
    Принимает callback от нажатия кнопок в keyboards.size_keyboard
    :param client: Клиент для работы с телеграмом
    :param query: действие пользователя которое запустило эту функцию
    :return:
    """
    watermark_db.set_setting(query.from_user.id, 'color', query.data.split('=')[1])
    await client.answer_callback_query(query.id, text=f'Цвет установлен!')


@Client.on_message(filters.regex(pattern='^.*размер.*$') & filters.private & utils.check_user
                   & utils.task_type_filter(type_name='watermark'))
async def size_select(_, message):
    """
    Присылает клавиатуру выбора размера логотипа
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    await message.reply('Выбери цвет:', reply_markup=keyboards.size_keyboard)


@Client.on_callback_query(watermark_utils.new_size & utils.check_user
                          & utils.task_type_filter(type_name='watermark'))
async def size_callback(client, query):
    """
    Принимает callback от нажатия кнопок в keyboards.size_keyboard
    :param client: Клиент для работы с телеграмом
    :param query: действие пользователя которое запустило эту функцию
    :return:
    """
    watermark_db.set_setting(query.from_user.id, 'size', str(int(query.data.split('=')[1])))
    await client.answer_callback_query(query.id, text=f'Размер установлен!')


@Client.on_message(filters.regex(pattern='^.*режим.*$') & filters.private & utils.check_user
                   & utils.task_type_filter(type_name='watermark'))
async def mode_select(_, message):
    """
    Присылает клавиатуру выбора режима логотипа
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    user = watermark_db.get_user(message.from_user.id)
    await message.reply('Выбери режим добавления логотипа:', reply_markup=keyboards.modes_keyboard[user[2]])


@Client.on_callback_query(watermark_utils.new_mode & utils.check_user
                          & utils.task_type_filter(type_name='watermark'))
async def mode_callback(client, query):
    """
    Принимает callback от нажатия кнопок в keyboards.modes_keyboard
    :param client: Клиент для работы с телеграмом
    :param query: действие пользователя которое запустило эту функцию
    :return:
    """
    watermark_db.set_setting(query.from_user.id, 'mode', query.data.split('=')[1])
    await client.answer_callback_query(query.id, text=f'Режим установлен!')
