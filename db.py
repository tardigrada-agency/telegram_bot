# from mongoengine.fields import StringField, IntField
# from mongoengine import Document
# from mongoengine import connect
# import config
import psycopg2
import os


connection = psycopg2.connect(
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT'],
    database=os.environ['POSTGRES_DB']
)

cursor = connection.cursor()


def add_user(telegram_id: int, username: str = None, name: str = '', position: str = '', is_admin: bool = False):
    """
    Добавляет юзера в базу
    :param is_admin: True если пользователь админ
    :param position: Должность пользователя в медиа
    :param name: Имя пользователя
    :param username: username пользователя в telegram
    :param telegram_id: Ид пользователя в telegram
    :return:
    """
    cursor.execute('INSERT INTO users (telegram_id, username, name, position, is_admin) '
                   'VALUES (%s::integer, %s, %s, %s, %s)', [telegram_id, username, name, position, is_admin])
    connection.commit()


def get_user(telegram_id: int):
    """
    Получает юзера из базы
    :param telegram_id: Ид пользователя в telegram
    :return:
    """
    cursor.execute('SELECT telegram_id, username, name, position, is_admin, date, task_type '
                   'FROM users WHERE telegram_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return record


def check_user_in_users(telegram_id) -> bool:
    """
    Проверка есть ли юзер в базе
    :param telegram_id: Ид пользователя в telegram
    :return:
    """
    cursor.execute('SELECT telegram_id FROM users WHERE telegram_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return True if record else False


def set_task_type(telegram_id: int, task_type: str):
    cursor.execute(f"UPDATE users SET task_type = %s WHERE telegram_id = %s::integer;", [task_type, int(telegram_id)])
    connection.commit()


def add_activity(user_id: int, task_type: str, task_name: str, task_note: str, time_started: str, time_ended: str):
    """
    Добавление активности пользователя в базу
    :param user_id: ид пользователя
    :param task_type: тип задачи
    :param task_name: название задачи
    :param task_note: комментарий к задаче
    :param time_started: время начала задачи
    :param time_ended: время конца задачи
    :return:
    """
    cursor.execute('INSERT INTO activity (user_id, task_type, task_name, task_note, time_started, time_ended) '
                   'VALUES (%s::integer, %s, %s, %s, %s, %s)', [user_id, task_type, task_name,
                                                                task_note, time_started, time_ended])
    connection.commit()
