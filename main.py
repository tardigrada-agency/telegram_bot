from pyrogram import Client
import db
import os

#   Если в базе нет админа - добавим его
admin_id = int(os.environ['ADMIN_TELEGRAM_ID'])
if not db.check_user_in_users(admin_id):
    db.add_user(admin_id, is_admin=True)

#   Запускаем бота
plugins = dict(root='plugins')
app = Client(session_name=os.environ['PYROGRAM_SESSION_STRING'], api_id=os.environ['PYROGRAM_API_ID'],
             api_hash=os.environ['PYROGRAM_API_HASH'], plugins=plugins)
app.run()
