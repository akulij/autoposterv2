import os
import random
import time

from aiogram.types import InputMediaPhoto

from .types import ProductInfo
from .db import get_product_picture_links
from .builder import build_message
from .storer import set_renew_flag

from dotenv import load_dotenv

load_dotenv()
CHAT_ID = int(os.getenv("CHAT_ID"))
GENDER = os.getenv("GENDER")
assert GENDER in ["man", "woman"]

TOKENS = [
        "5558500501:AAFcvh2thvu3_R-TK9sqlr2QNaUrfWomZ8A",
        "5457322651:AAGAuMomAeSNqLIPxn1z27FUoMRqC7hG8-g",
        "5619328360:AAF1CuZvP_HuOA-pamLwK9t0b_ej6dUNsRk",
        ]
bots: list[Bot] = []
for token in TOKENS:
    bots.append(Bot(token))

async def publish_to_telegram(product: ProductInfo):
    msg = build_message(product, GENDER)

    plinks = get_product_picture_links(product.id)
    pictures = []
    for idx, link in enumerate(plinks):
        pictures.append(InputMediaPhoto(link, caption=msg if idx == 0 else None, parse_mode="HTML"))
    pictures = pictures[:4]
    # message = await random.choice(bots).send_photo(chat_id, photo=photo_url, caption=msg, reply_markup=keyboard, parse_mode="MARKDOWN")
    try:
        messages = await random.choice(bots).send_media_group(CHAT_ID, pictures)
        set_renew_flag(True)
        time.sleep(2)
        caption_message = messages[0]
        photo_messages = messages[1:]
        # for message_ in messages:
        #     if message_.caption:
        #         message = message_
        # message = await random.choice(bots).send_photo(chat_id, photo=photo_url, caption=msg, reply_markup=keyboard, parse_mode="MARKDOWN")
        chat_id = caption_message.chat.id
        msg_id = caption_message.message_id
        photo_infos = []
        for photo_msg in photo_messages:
            photo_infos.append((photo_msg.chat.id, photo_msg.message_id))

        return chat_id, msg_id, msg, photo_infos
        # create_post(product.id, chat_id, msg_id)
    except:
        pass

async def renew_telegram_post(chat_id: int, msg_id: int, product: ProductInfo, prev_text: str, photo_infos: list[tuple[int, int]]):
    pass
