from plugins.watermark import watermark_utils
from plugins.watermark import watermark_db
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
import utils
import time
import db


@Client.on_message(filters.photo & utils.check_user & utils.task_type_filter(type_name='watermark'))
async def photo(client, message):
    """
    Вызываеться когда пользователь прислал фотографию
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    started = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        user = watermark_db.get_user(message.from_user.id)    # Получаем юзера из базы

        # Удаляем фото с такимже file_unique_id если оно уже почему-то есть
        watermark_utils.remove_photo(message.photo.file_unique_id)

        # Скачиваем фото из телеграмма
        status = await message.reply_text('Скачал 0%')
        await download_photo(message.photo, client, status)

        # Обработка фотографии
        watermark_status = await watermark_utils.draw_logo_on_photo(f'{message.photo.file_unique_id}.jpg', user[4], user[1], user[2], user[3])
        if watermark_status['error']:
            await status.edit_text(watermark_status['status'])
        else:
            # Отправляем фото в телеграмм
            await client.send_chat_action(message.chat.id, action=ChatAction.UPLOAD_PHOTO)
            await client.send_photo(chat_id=message.from_user.id,
                                    photo=f'temp/{message.photo.file_unique_id}_logo.jpg',
                                    progress=watermark_utils.upload_callback, progress_args=(status,))
            await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    watermark_utils.remove_photo(message.photo.file_unique_id)  # Удаляем фото, оно нам больше не нужно

    #   Добавляем действи пользователя в базу
    ended = time.strftime('%Y-%m-%d %H:%M:%S')
    db.add_activity(message.from_user.id, 'watermark', 'photo_as_image',
                    f'file_unique_id={message.photo.file_unique_id}', started, ended)


@Client.on_message(watermark_utils.document_image & utils.check_user & utils.task_type_filter(type_name='watermark'))
async def photo_document(client, message):
    """
    Вызываеться когда пользователь прислал фотографию как документ
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    started = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        user = watermark_db.get_user(message.from_user.id)    # Получаем юзера из базы

        # Удаляем фото с такимже file_unique_id если оно уже почему-то есть
        watermark_utils.remove_photo(message.document.file_unique_id)

        # Скачиваем фото из телеграмма
        status = await message.reply_text('Скачал 0%')
        await download_photo(message.document, client, status)

        # Обработка фотографии
        await status.edit_text('Обработка...')
        watermark_status = await watermark_utils.draw_logo_on_photo(f'{message.document.file_unique_id}.jpg', user[4],
                                                                    user[1], user[2], user[3])
        if watermark_status['error']:
            await status.edit_text(watermark_status['status'])
        else:
            # Отправляем фото в телеграмм
            await client.send_chat_action(message.chat.id, action=ChatAction.UPLOAD_PHOTO)
            await client.send_document(chat_id=message.from_user.id,
                                       document=f'temp/{message.document.file_unique_id}_logo.jpg',
                                       file_name=f'{message.document.file_name.split(".")[0]}_logo.jpg',
                                       progress=watermark_utils.upload_callback, progress_args=(status,))
            await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    watermark_utils.remove_photo(message.document.file_unique_id)  # Удаляем фото, оно нам больше не нужно

    #   Добавляем действи пользователя в базу
    ended = time.strftime('%Y-%m-%d %H:%M:%S')
    db.add_activity(message.from_user.id, 'watermark', 'photo_as_document',
                    f'file_unique_id={message.document.file_unique_id}', started, ended)


async def download_photo(file, client, status):
    """
    Функция для скачивания файла с сервера телеграмм
    :param status: : Сообщение чтобы показывать юзеру что происходит
    :param file: Файл который нужно скачать
    :param client: Клиент для общения с телеграммом
    :return:
    """
    await client.download_media(message=file, file_name=f'temp/{file.file_unique_id}.jpg',
                                progress=watermark_utils.download_callback, progress_args=(status,))
