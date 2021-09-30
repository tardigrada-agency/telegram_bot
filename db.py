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
    :param is_admin: True если пользователь admin
    :param position: Должность пользователя в медиа
    :param name: Имя пользователя
    :param username: username пользователя в telegram
    :param telegram_id: Ид пользователя в telegram
    """
    cursor.execute('INSERT INTO users (telegram_id, username, name, position, is_admin) '
                   'VALUES (%s::integer, %s, %s, %s, %s)', [telegram_id, username, name, position, is_admin])
    connection.commit()


def delete_user(telegram_id: int):
    """
    Удаления юзера из базы
    :param telegram_id: Ид пользователя в telegram
    """
    cursor.execute('DELETE FROM users WHERE telegram_id=%s::integer', [telegram_id])
    connection.commit()


def get_user(telegram_id: int):
    """
    Получает юзера из базы
    :param telegram_id: Ид пользователя в telegram
    """
    cursor.execute('SELECT telegram_id, username, name, position, is_admin, date, task_type '
                   'FROM users WHERE telegram_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return record


def get_users():
    """
    Получает всех юзеров из базы
    """
    cursor.execute('SELECT telegram_id, username, name, position, is_admin, date, task_type FROM users')
    record = cursor.fetchall()
    return record


def user_is_admin(telegram_id: int) -> bool:
    """
    Проверка  юзер админ или нет
    :param telegram_id: Ид пользователя в telegram
    :return: True если юзер админ
    """
    cursor.execute('SELECT is_admin FROM users WHERE telegram_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return record[0] if record else False


def get_username(telegram_id: int) -> str:
    """
    Получение username юзера из базы
    :param telegram_id: Ид пользователя в telegram
    :return: username
    """
    cursor.execute('SELECT username FROM users WHERE telegram_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return record[0]


def set_username(telegram_id: int, new_username: str):
    """
    Установка нового username в базу
    """
    cursor.execute(f"UPDATE users SET username = %s WHERE telegram_id = %s::integer;", [new_username, int(telegram_id)])
    connection.commit()


def check_user_in_users(telegram_id: int) -> bool:
    """
    Проверка есть ли юзер в базе
    :param telegram_id: Ид пользователя в telegram
    :return: True если юзер в базе
    """
    cursor.execute('SELECT telegram_id FROM users WHERE telegram_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return True if record else False


def set_task_type(telegram_id: int, task_type: str):
    """
    Утановка нового типа задачи для юзера
    :param telegram_id: Ид юзера в телеграм
    :param task_type: Новый тип задачи который нужно устоновить
    """
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
    """
    cursor.execute('INSERT INTO activity (user_id, task_type, task_name, task_note, time_started, time_ended) '
                   'VALUES (%s::integer, %s, %s, %s, %s, %s)', [user_id, task_type, task_name,
                                                                task_note, time_started, time_ended])
    connection.commit()
