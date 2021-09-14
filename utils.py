from pyrogram import filters
import db

check_user = filters.create(lambda _, __, message: db.check_user_in_users(message.from_user.id))


def task_type_filter(type_name):
    async def task_type(_, __, message):
        user = db.get_user(message.from_user.id)
        return True if user[6] == type_name else False

    return filters.create(task_type, type_name=type_name)

