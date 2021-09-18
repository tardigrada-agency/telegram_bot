from plugins.jinja2png import keyboards
from pyrogram import filters
import requests
import pyrogram
import os

set_template = filters.create(lambda _, __, data: data.data.split("=")[0] == 'set_template')
if 'JINJA2PNG_HOST' in os.environ.keys():
    url = f"http://{os.environ['JINJA2PNG_HOST']}:{os.environ['JINJA2PNG_PORT']}/template/list"
text_command = filters.create(lambda _, __, message: message.text in keyboards.menu)


def get_template_list() -> list:
    response = requests.request("GET", url).json()
    return response


async def download_photo(file, client):
    """
    Функция для скачивания файла с сервера телеграмм
    :param file: Файл который нужно скачать
    :param client: Клиент для общения с телеграммом
    :return:
    """
    await client.download_media(message=file, file_name=f'temp/{file.file_unique_id}.jpg')


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
    remove_file(f'temp/{file_id}.png')


async def download_callback(current, total, status):
    """
    Callback чтобы показывать юзеру % скачивания файла на сервер
    :param current:
    :param total:
    :param status:
    :return:
    """
    try:
        await status.edit_text(f'Скачал {int((current / total) * 100)}%')
    except pyrogram.errors.exceptions.bad_request_400.MessageNotModified:
        pass


async def upload_callback(current, total, status):
    """
    Callback чтобы показывать юзеру % загрузки файла на сервер
    :param current:
    :param total:
    :param status:
    :return:
    """
    try:
        await status.edit_text(f'Загрузил {int((current / total) * 100)}%')
    except pyrogram.errors.exceptions.bad_request_400.MessageNotModified:
        pass
