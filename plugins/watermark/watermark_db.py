from db import connection, cursor


def set_setting(telegram_id: int, setting_name: str, value: str):
    """
    Получает юзера из базы
    :param telegram_id: Ид пользователя в telegram
    :param setting_name: Название настройки которую нужно поменять
    :param value: Значение которое нужно установить
    :return:
    """
    cursor.execute(f"UPDATE watermark SET {setting_name} = %s WHERE user_id = %s::integer;", [value, int(telegram_id)])
    connection.commit()


def get_user(telegram_id: int):
    """
    Получает юзера из базы
    :param telegram_id: Ид пользователя в telegram
    :return:
    """
    cursor.execute('SELECT user_id, color, type, mode, size '
                   'FROM watermark WHERE user_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return record


def check_user(telegram_id) -> bool:
    """
    Проверка есть ли юзер в базе
    :param telegram_id: ID пользователя в telegram
    :return:
    """
    cursor.execute('SELECT user_id FROM watermark WHERE user_id=%s::integer', [int(telegram_id)])
    record = cursor.fetchone()
    return True if record else False


def add_user(user_id: int, color: str, logo_type: str, mode: str, size: int):
    """
    Добавление юзера в базу
    :param size: размер логотипа
    :param mode: режим добавление логотипа
    :param logo_type: тип логотипа
    :param color: цвет логотипа
    :param user_id: Ид пользователя в telegram
    :return:
    """
    cursor.execute("INSERT INTO watermark (user_id, color, type, mode, size) "
                   "VALUES (%s::integer, %s, %s, %s, %s::integer);", [int(user_id), color, logo_type, mode, int(size)])
    connection.commit()


def delete_user(telegram_id: int):
    """
    Удаления юзера из базы
    :param telegram_id: Ид пользователя в telegram
    """
    cursor.execute('DELETE FROM watermark WHERE telegram_id=%s::integer', [telegram_id])
    connection.commit()
