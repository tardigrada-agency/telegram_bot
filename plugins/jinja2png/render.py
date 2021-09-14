from plugins.jinja2png import jinja2png_utils
from plugins.jinja2png import jinja2png_db
from pyrogram import Client, filters
from io import open as iopen
import requests
import base64
import utils
import uuid
import json
import time
import db
import os

url = f"http://{os.environ['JINJA2PNG_HOST']}:{os.environ['JINJA2PNG_PORT']}/template/render/"

headers = {
    'Content-Type': 'application/json'
}


@Client.on_message(filters.text & filters.private & utils.check_user
                   & utils.task_type_filter(type_name='jinja2png') & ~jinja2png_utils.text_command)
async def text(client, message):
    """
    Присылает клавиатуру выбора языка логотипа
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    started = time.strftime('%Y-%m-%d %H:%M:%S')
    payload = json.dumps({
        "texts": message.text.split('\n\n'),
        "images": [
        ]
    })
    user_template = jinja2png_db.get_user(message.from_user.id)[1]
    response = requests.request("POST", url + user_template, headers=headers,
                                data=payload)

    image_uuid = uuid.uuid4()
    jinja2png_utils.remove_photo(image_uuid)

    with iopen(f'temp/{image_uuid}.png', 'wb') as file:
        file.write(response.content)

    await client.send_chat_action(message.chat.id, action='upload_document')
    await client.send_document(message.from_user.id, f'temp/{image_uuid}.png')
    if not os.path.exists(f'temp/{image_uuid}.png'):
        os.remove(f'temp/{image_uuid}.png')
    ended = time.strftime('%Y-%m-%d %H:%M:%S')
    db.add_activity(message.from_user.id, 'jinja2png', 'jinja2png_text',
                    f'text={message.text}', started, ended)


@Client.on_message(filters.photo & utils.check_user & utils.task_type_filter(type_name='jinja2png'))
async def photo(client, message):
    """
    Вызываеться когда пользователь прислал фотографию как документ
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    started = time.strftime('%Y-%m-%d %H:%M:%S')
    if not message.caption:
        await message.reply_text('Для обложки нужна подпись, пришли фотографию с подписью в одном сообщение')
        return
    jinja2png_utils.remove_photo(message.photo.file_unique_id)
    await jinja2png_utils.download_photo(message.photo, client)
    base64_image = get_base64_encoded_image(f'temp/{message.photo.file_unique_id}.jpg')
    payload = json.dumps({
        "texts": message.caption.split('\n\n'),
        "images": [
            f"data:image/jpeg;base64,{base64_image}"
        ]
    })

    response = requests.request("POST", url + jinja2png_db.get_user(message.from_user.id)[1],
                                headers=headers, data=payload)

    # Saving response
    image_uuid = uuid.uuid4()
    jinja2png_utils.remove_photo(image_uuid)
    with iopen(f'temp/{image_uuid}.png', 'wb') as file:
        file.write(response.content)

    # Sending photo to telegram
    await client.send_chat_action(message.chat.id, action='upload_document')
    await client.send_document(message.from_user.id, f'temp/{image_uuid}.png')

    # Deleting photo
    jinja2png_utils.remove_photo(image_uuid)
    jinja2png_utils.remove_photo(message.photo.file_unique_id)
    ended = time.strftime('%Y-%m-%d %H:%M:%S')
    db.add_activity(message.from_user.id, 'jinja2png', 'jinja2png_image_text',
                    f'text={message.caption};photo={message.photo.file_unique_id}', started, ended)


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
