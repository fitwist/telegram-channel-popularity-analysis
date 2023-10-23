from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
# import pandas as pd
import json

BATCHES = 10000 # Число итераций

api_id = '142422' # Идентификатор приложения
api_hash = '45acf455c700c880de7a3ce5c91fd7dc'

name = 'Helen Kapatsa' # Название сессии
chat = 'prog_point'


client = TelegramClient('data_analysis_session',
                    api_id,
                    api_hash,
                    )

client.connect()

# Авторизуемся
if not client.is_user_authorized():
    client.send_code_request('+79627276037')
    me = client.sign_in('+79627276037', input('Введи код: '))

channel_username='a_cup_of_java'
channel_entity=client.get_entity(channel_username)

batch_count = 0 # Номер пакета записей

while batch_count <= BATCHES:
    # Отправим запрос на получение массивов о постах
    posts = client(GetHistoryRequest(
        peer=channel_entity,
        limit=100,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=batch_count,
        hash=0))

    i = 0

    
    while i <= len(posts.messages) - 1:
        emojis = []
        
        j = 0

        # Выделим число реакций и их типы
        while j <= 10:
            try:
                reaction = {
                    "emojis": posts.messages[i].reactions.results[j].reaction.emoticon,
                    "emoji_count": posts.messages[i].reactions.results[j].count,
                }
                emojis.append(reaction)
                j += 1
            except (AttributeError, TypeError, IndexError) as error:
                j += 1
        
        # Выделим число комментариев и заполним пустоты
        try:
            replies = posts.messages[i].replies.replies
        except AttributeError:
            replies = 0

        post = {
            "id": posts.messages[i].id,
            "date": str(posts.messages[i].date),
            "message": posts.messages[i].message,
            "views": posts.messages[i].views,
            "forwards": posts.messages[i].forwards,
            "replies": replies,
            "reactions": emojis
        }

        with open(f"{post['id']}.json", "w") as outfile:
            json.dump(post, outfile, ensure_ascii=False)
        
        i += 1
    batch_count += 1