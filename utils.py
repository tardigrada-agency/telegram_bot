from dataclasses import dataclass
from pyrogram import filters
import datetime
import db

check_user = filters.create(lambda _, __, message: db.check_user_in_users(message.from_user.id))
user_is_admin = filters.create(lambda _, __, message: db.user_is_admin(message.from_user.id))


@dataclass
class User:
    telegram_id: int
    username: str = ""
    name: str = ""
    position: str = ""
    is_admin: bool = False

    def add_to_db(self):
        if not db.check_user_in_users(self.telegram_id):
            db.add_user(self.telegram_id, self.username, self.name, self.position, self.is_admin)


def task_type_filter(type_name):
    async def task_type(_, __, message):
        user = db.get_user(message.from_user.id)
        return True if user[6] == type_name else False

    return filters.create(task_type, type_name=type_name)


def update_username_in_db_if_not_matches(telegram_id: int, username: str):
    """
    Обновляет username в базе если он не совпадает со старым
    :param telegram_id: Ид пользователя в telegram
    :param username: актуальный username из telegram
    """
    old_username: str = db.get_username(telegram_id)
    if old_username != username:
        db.set_username(telegram_id, username)
