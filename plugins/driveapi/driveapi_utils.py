from plugins.driveapi import keyboards
from pyrogram import filters
import pyrogram
import shutil
import os

text_command = filters.create(lambda _, __, message: message.text in keyboards.menu)


def remove_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)


def remove_file(path: str):
    if os.path.isfile(path):
        os.remove(path)


def remove_photo(file_id):
    """
    Удаляем фото для file_id
    :param file_id: Ид файлы который должен быть удален
    :return:
    """
    remove_file(f'temp/{file_id}.jpg')


async def download_callback(current, total, status, name=''):
    """
    Callback чтобы показывать юзеру % скачивания файла на сервер
    :param current:
    :param total:
    :param status:
    :param name:
    :return:
    """
    try:
        await status.edit_text(f'Скачал {f"{name} на " if name else ""}{int((current / total) * 100)}%')
    except Exception as e:
        print(e)


async def upload_callback(current, total, status, name=''):
    """
    Callback чтобы показывать юзеру % загрузки файла на сервер
    :param current:
    :param total:
    :param status:
    :return:
    """
    try:
        await status.edit_text(f'Загрузил {f"{name} на " if name else ""}{int((current / total) * 100)}%')
    except pyrogram.errors.exceptions.bad_request_400.MessageNotModified:
        pass
