from plugins.watermark import watermark_utils
from plugins.watermark import watermark_db
from pyrogram import Client
from pyrogram.enums import ChatAction
import zipfile
import shutil
import utils
import re
import db
import os


@Client.on_message(watermark_utils.document_zip & utils.check_user
                   & utils.task_type_filter(type_name='watermark'))
async def zip_file(client, message):
    """
    Добавляет ватермарку на все файлы в zip архиве
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    watermark_utils.remove_zip(message.document.file_unique_id)  # Удаляем архив с таким ид если оно уже почему-то есть
    try:
        error = False
        user = watermark_db.get_user(message.from_user.id)  # Получаем юзера из базы
        re_photo = re.compile(r'(^.*\.)(jpe?g|png)')
        re_video = re.compile(r'(^.*\.)(mov|mp4|avi)')

        # Скачиваем архив
        status = await message.reply_text('Скачал 0%')
        await download_zip(message.document, client, status)

        # Раскрываем архив
        os.mkdir(f'temp/{message.document.file_unique_id}')
        await status.edit_text('Распаковка...')
        with zipfile.ZipFile(f'temp/{message.document.file_unique_id}.zip', 'r') as zipObj:
            zipObj.extractall(f'temp/{message.document.file_unique_id}/')

        os.mkdir(f'temp/{message.document.file_unique_id}_logo')  # Создаем папку для файлов с логотипом

        #   Для всех файлов из архива запускам ffmpeg
        path = f'temp/{message.document.file_unique_id}'
        for root, dirs, files in os.walk(path):
            for file in files:
                if error:
                    break
                if re_video.match(file.lower()):
                    await status.edit_text(f'Обработка видео {file}')
                    watermark_status = await watermark_utils.draw_logo_on_video(file,
                                                                                user[4], user[1], user[2], user[3],
                                                                                folder=message.document.file_unique_id)
                    if watermark_status['error']:
                        await status.edit_text(watermark_status['status'])
                        error = True
                        break
                elif re_photo.match(file.lower()):
                    await status.edit_text(f'Обработка фотографии {file}')
                    watermark_status = await watermark_utils.draw_logo_on_photo(file,
                                                                                user[4], user[1], user[2], user[3],
                                                                                folder=message.document.file_unique_id)
                    if watermark_status['error']:
                        await status.edit_text(watermark_status['status'])
                        error = True
                        break
                else:
                    await status.edit_text(f'Копирование {file} без добавление ватермарки')
                    shutil.move(f'temp/{message.document.file_unique_id}/{file}',
                                f'temp/{message.document.file_unique_id}_logo/{file}')
        if not error:
            #  Создаем новый архив из файлоы с логотипом
            await status.edit_text(f'Архивация...')
            await zip_dir(message.document.file_unique_id)

            #   Отправляем архив
            await client.send_chat_action(message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
            await client.send_document(chat_id=message.from_user.id,
                                       document=f'temp/{message.document.file_unique_id}_logo.zip',
                                       file_name=f'{watermark_utils.get_filename(message.document.file_name)}_logo.zip',
                                       progress=watermark_utils.upload_callback, progress_args=(status,))
            await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    watermark_utils.remove_zip(message.document.file_unique_id)  # Удаляем архив, оно нам больше не нужно


async def download_zip(file, client, status):
    """
    Функция для скачивания файла с сервера телеграмм
    :param status: : Сообщение чтобы показывать юзеру что происходит
    :param file: Файл который нужно скачать
    :param client: Клиент для общения с телеграммом
    :return:
    """
    await client.download_media(message=file, file_name=f'temp/{file.file_unique_id}.zip',
                                progress=watermark_utils.download_callback, progress_args=(status,))


async def zip_dir(file_id):
    """
    Создает зип архив ./temp/{file_id}_logo.zip из папки ./temp/{file_id}_logo
    :param file_id: Ид изначального архива
    :return:
    """
    zip_archive = zipfile.ZipFile(f'./temp/{file_id}_logo.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(f'./temp/{file_id}_logo'):
        for file in files:
            zip_archive.write(os.path.join(root, file), arcname=file)
    zip_archive.close()
