from pyrogram.types import InputMediaDocument
from plugins.driveapi import driveapi_utils
from pyrogram import Client, filters
from io import open as iopen
import pyrogram
import requests
import zipfile
import asyncio
import utils
import time
import json
import uuid
import sys
import os
import db


@Client.on_message(filters.text & filters.private & utils.check_user
                   & utils.task_type_filter(type_name='driveapi') & ~driveapi_utils.text_command)
async def text(client, message):
    """
    Присылает клавиатуру выбора языка логотипа
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    started = time.strftime('%Y-%m-%d %H:%M:%S')
    url = f"http://{os.environ['DRIVEAPI_HOST']}:{os.environ['DRIVEAPI_PORT']}/getphoto"

    payload = json.dumps({
        "name": message.text
    })
    headers = {
        'Content-Type': 'application/json'
    }
    status = await message.reply_text('Ищу...')

    # Генерируем uuid запроса
    file_uuid = uuid.uuid4()
    driveapi_utils.remove_photo(file_uuid)

    # Создаем запрос
    response = requests.post(url, stream=True, headers=headers, data=payload)
    total_length = response.headers.get('content-length')

    # Получаем тип файла
    file_type = 'data'
    if response.headers['Content-Type'].split('/')[1] == 'jpeg':
        file_type = 'jpg'
    elif response.headers['Content-Type'].split('/')[1] == 'zip':
        file_type = 'zip'
    elif response.headers['Content-Type'].split('/')[1].split(';')[0] == 'json':
        await status.edit_text(json.loads(response.text)['message'])
        return
    else:
        await status.edit_text('Какая-то ошибка, ничего больше ничего сказать не могу :(')
        return

    # Открываем файл на запись
    with open(f'temp/{file_uuid}.{file_type}', "wb") as f:
        if total_length is None:  # Если длина файла не известна, то скачиваем разом
            await status.edit_text("content-length не указан в файле, не выйдет показать прогресс скачивания :(")
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)

            # Скачиваем файлами блоками по 524287
            for data in response.iter_content(chunk_size=524287):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                try:
                    await status.edit_text(f"Скачал {int((dl / total_length) * 100)}%")
                except pyrogram.errors.exceptions.bad_request_400.MessageNotModified:
                    pass

    if file_type == 'jpg':  # Если картинка, то отрпавим ее
        await client.send_chat_action(message.chat.id, action='upload_document')
        await client.send_document(message.from_user.id, f'temp/{file_uuid}.{file_type}',
                                   file_name=f'{message.text.replace(" ", "_")}.{file_type}',
                                   progress=driveapi_utils.upload_callback, progress_args=(status,))
        driveapi_utils.remove_file(f'temp/{file_uuid}.{file_type}')
    if file_type == 'zip':  # Если zip архив, то сначало распакуем его
        os.mkdir(f'temp/{file_uuid}')
        await status.edit_text('Распаковка...')
        with zipfile.ZipFile(f'temp/{file_uuid}.{file_type}', 'r') as zipObj:
            zipObj.extractall(f'temp/{file_uuid}/')
        await status.edit_text('Подготовка к загрузке...')
        path = f'temp/{file_uuid}/'

        # Отправим все файлы из архива
        for root, dirs, files in os.walk(path):
            for file in files:
                await client.send_chat_action(message.chat.id, action='upload_document')
                await client.send_document(message.from_user.id, f'temp/{file_uuid}/{file}',
                                           file_name=file,
                                           progress=driveapi_utils.upload_callback, progress_args=(status, file))
        # Удаляем папку
        driveapi_utils.remove_dir(f'temp/{file_uuid}/')
    driveapi_utils.remove_file(f'temp/{file_uuid}.{file_type}')  # Удялем файл
    await status.delete()   # Удаляем статусное сообщение

    # Запись действий в лог
    ended = time.strftime('%Y-%m-%d %H:%M:%S')
    db.add_activity(message.from_user.id, 'driveapi', f'driveapi_{file_type}',
                    f'request={message.text}', started, ended)
