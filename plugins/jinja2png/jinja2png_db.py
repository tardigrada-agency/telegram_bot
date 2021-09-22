from db import connection, cursor


def set_jinja2png_setting(telegram_id: int, value: str):
    """
    Получает юзера из базы
    :param telegram_id: Ид пользователя в telegram
    :param value: Значение которое нужно установить
    :return:
    """
    cursor.execute(f"UPDATE jinja2png SET template = %s WHERE user_id = %s::integer;", [value, int(telegram_id)])
    connection.commit()


def get_user(telegram_id: int):
    """
    Получает юзера из базы
    :param telegram_id: Ид пользователя в telegram
    :return:
    """
    cursor.execute('SELECT user_id, template '
                   'FROM jinja2png WHERE user_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return record


def check_user(telegram_id) -> bool:
    """
    Проверка есть ли юзер в базе
    :param telegram_id: Ид пользователя в telegram
    :return:
    """
    cursor.execute('SELECT user_id FROM jinja2png WHERE user_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return True if record else False


def add_user(user_id: int, template: str):
    """
    Добавление юзера в базу
    :param template: шаблон
    :param user_id: Ид пользователя в telegram
    :return:
    """
    cursor.execute("INSERT INTO jinja2png (user_id, template) VALUES (%s::integer, %s);", [int(user_id), template])
    connection.commit()


def delete_user(telegram_id: int):
    """
    Удаления юзера из базы
    :param telegram_id: Ид пользователя в telegram
    """
    cursor.execute('DELETE FROM jinja2png WHERE telegram_id=%s::integer', [telegram_id])
    connection.commit()
