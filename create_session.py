from pyrogram import Client
import logging
import os

# Starting bot
plugins = dict(root='plugins')
with Client(':memory:', api_id=os.environ['PYROGRAM_API_ID'],
            api_hash=os.environ['PYROGRAM_API_HASH']) as app:
    logging.info(f'@{app.get_me()["username"]} session created')
