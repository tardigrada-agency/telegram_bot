from plugins.watermark import watermark_utils
from plugins.watermark import watermark_db
from pyrogram import Client, filters
import utils
import time
import db


@Client.on_message(filters.video & utils.check_user & utils.task_type_filter(type_name='watermark'))
async def video(client, message):
    """
    Добавляет ватермарку на видео
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    started = time.strftime('%Y-%m-%d %H:%M:%S')
    watermark_utils.remove_video(message.video.file_unique_id)  # Удаляем видео с таким ид если оно уже почему-то есть
    try:
        user = watermark_db.get_user(message.from_user.id)    # Получаем юзера из базы

        # Скачиваем видео из телеграмма
        status = await message.reply_text('Скачал 0%')
        await download_video(message.video, client, status)

        # Запукаем ffmpeg для нашего видео
        await status.edit_text('Обработка...')
        watermark_status = await watermark_utils.draw_logo_on_video(f'{message.video.file_unique_id}.mp4',
                                                                    user[4], user[1], user[2], user[3])
        if watermark_status['error']:
            await status.edit_text(watermark_status['status'])
        else:
            # Загружаем видео обратно в телеграмм
            await client.send_chat_action(message.chat.id, action='upload_video')
            await client.send_video(chat_id=message.from_user.id,
                                    video=f'temp/{message.video.file_unique_id}_logo.mp4',
                                    progress=watermark_utils.upload_callback, progress_args=(status,))
            await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    watermark_utils.remove_video(message.video.file_unique_id)   # Удаляем видео, оно нам больше не нужно

    #   Добавляем действи пользователя в базу
    ended = time.strftime('%Y-%m-%d %H:%M:%S')
    db.add_activity(message.from_user.id, 'watermark', 'video_as_video',
                    f'file_unique_id={message.video.file_unique_id}', started, ended)


@Client.on_message(watermark_utils.document_video & utils.check_user & utils.task_type_filter(type_name='watermark'))
async def video_document(client, message):
    """
    Добавляет ватермарку на видео как документ
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    started = time.strftime('%Y-%m-%d %H:%M:%S')
    # Удаляем видео с таким ид если оно уже почему-то есть
    watermark_utils.remove_video(message.document.file_unique_id)
    try:
        user = watermark_db.get_user(message.from_user.id)    # Получаем юзера из базы

        # Скачиваем видео из телеграмма
        status = await message.reply_text('Скачал 0%')
        await download_video(message.document, client, status)

        # Запукаем ffmpeg для нашего видео
        watermark_status = await watermark_utils.draw_logo_on_video(f'{message.document.file_unique_id}.mp4',
                                                                    user[4], user[1], user[2], user[3])
        if watermark_status['error']:
            await status.edit_text(watermark_status['status'])
        else:
            # Загружаем видео обратно в телеграмм
            await client.send_chat_action(message.chat.id, action='upload_video')
            await client.send_document(chat_id=message.from_user.id,
                                       document=f'temp/{message.document.file_unique_id}_logo.mp4',
                                       file_name=f'{message.document.file_name.split(".")[0]}_logo.mp4',
                                       progress=watermark_utils.upload_callback, progress_args=(status,))
        await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    watermark_utils.remove_video(message.document.file_unique_id)   # Удаляем видео, оно нам больше не нужно

    #   Добавляем действи пользователя в базу
    ended = time.strftime('%Y-%m-%d %H:%M:%S')
    db.add_activity(message.from_user.id, 'watermark', 'video_as_document',
                    f'file_unique_id={message.document.file_unique_id}', started, ended)


async def download_video(file, client, status):
    """
    Функция для скачивания файла с сервера телеграмм
    :param status: : Сообщение чтобы показывать юзеру что происходит
    :param file: Файл который нужно скачать
    :param client: Клиент для общения с телеграммом
    :return:
    """
    await client.download_media(message=file, file_name=f'temp/{file.file_unique_id}.mp4',
                                progress=watermark_utils.download_callback, progress_args=(status,))
