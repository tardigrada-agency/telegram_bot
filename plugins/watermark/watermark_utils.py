from plugins.watermark import modes
from pyrogram import filters
import subprocess as sp
import requests
import pyrogram
import shutil
import json
import os

# Custom filters
new_type = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_type')
new_size = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_size')
new_mode = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_mode')
new_color = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_color')
document_video = filters.create(
    lambda _, __, message: message.document.mime_type.split("/")[0] == 'video' if message.document else False)
document_image = filters.create(
    lambda _, __, message: message.document.mime_type.split("/")[0] == 'image' if message.document else False)
document_zip = filters.create(
    lambda _, __, message: message.document.mime_type == 'application/zip' if message.document else False)


def is_json(s: str):
    try:
        json_object = json.loads(s)
    except ValueError as e:
        return False
    return True


def get_filename(path: str) -> str:
    base = os.path.basename(path)
    return os.path.splitext(base)[0]


def remove_file(path: str):
    if os.path.isfile(path):
        os.remove(path)


def remove_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)


def remove_video(file_id):
    """
    Удаляем видео для file_id
    :param file_id: Ид файлы который должен быть удален
    :return:
    """
    remove_file(f'temp/{file_id}.mp4')
    remove_file(f'temp/{file_id}_logo.mp4')


def remove_photo(file_id):
    """
    Удаляем фото для file_id
    :param file_id: Ид файлы который должен быть удален
    :return:
    """
    remove_file(f'temp/{file_id}.jpg')
    remove_file(f'temp/{file_id}_logo.jpg')


def remove_zip(file_id):
    """
    Удаляет все файла/папки после работы с zip архивом
    :param file_id:
    :return:
    """
    remove_dir(f'./temp/{file_id}')
    remove_dir(f'./temp/{file_id}_logo')
    remove_file(f'./temp/{file_id}.zip')
    remove_file(f'./temp/{file_id}_logo.zip')


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


async def draw_logo_on_photo(file, size, color, logo_type, mode, folder='') -> bool:
    """
    Функция добавления логотипа размера: size, цвета: color, языка: lang на фото
    :param mode: Режим добавление логотипа
    :param folder: Папка где лежит фотография
    :param file: Ид фотографии
    :param size: Размер логотипа
    :param color: Цвет логотипа
    :param logo_type: Язык логотипа
    :return:
    """
    url = f"http://{os.environ['WATERMARK_HOST']}:{os.environ['WATERMARK_PORT']}" \
          f"/watermark_on_photo/{size}/{color}/{logo_type}/{mode}"

    payload = {}
    files = [
        ('file',
         (file, open(f'temp/{folder + "/" if folder else ""}{file}', 'rb'), 'application/octet-stream'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    response_text = response.text
    if is_json(response_text):
        status = json.loads(response_text)
        return status

    with open(f'temp/{folder+"_logo/" if folder else ""}{get_filename(file)}_logo.jpg', 'wb') as file:
        file.write(response.content)

    return {'error': False, 'status': ''}


async def draw_logo_on_video(file, size, color, logo_type, mode, folder='') -> bool:
    """
    Функция добавления логотипа размера: size, цвета: color, языка: lang на видео
    :param mode: Режим добавление логотипа
    :param folder: Папка где лежит фотография
    :param file: Ид фотографии
    :param size: Размер логотипа
    :param color: Цвет логотипа
    :param logo_type: Язык логотипа
    :return:
    """
    url = f"http://{os.environ['WATERMARK_HOST']}:{os.environ['WATERMARK_PORT']}" \
          f"/watermark_on_video/{size}/{color}/{logo_type}/{mode}"

    payload = {}
    files = [
        ('file',
         (file, open(f'temp/{folder + "/" if folder else ""}{file}', 'rb'), 'application/octet-stream'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    response_text = response.text
    if is_json(response_text):
        status = json.loads(response_text)
        return status

    with open(f'temp/{folder+"_logo/" if folder else ""}{get_filename(file)}_logo.mp4', 'wb') as file:
        file.write(response.content)

    return {'error': False, 'status': ''}
