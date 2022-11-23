import os
import random
import time
from typing import Literal

from aiogram.types import InputMediaPhoto

from .types import ProductInfo
from .db import get_product_picture_links
from .builder import build_message, build_sale_message
from .storer import set_renew_flag

from dotenv import load_dotenv

load_dotenv()
CHAT_ID = int(os.getenv("CHAT_ID"))
GENDER: Literal["man", "woman"] = os.getenv("GENDER")
assert GENDER in ["man", "woman"]

TOKENS = [
        "5558500501:AAFcvh2thvu3_R-TK9sqlr2QNaUrfWomZ8A",
        "5457322651:AAGAuMomAeSNqLIPxn1z27FUoMRqC7hG8-g",
        "5619328360:AAF1CuZvP_HuOA-pamLwK9t0b_ej6dUNsRk",
        ]
bots: list[Bot] = []
for token in TOKENS:
    bots.append(Bot(token))

async def publish_to_telegram(product: ProductInfo, is_sale: bool = False) -> tuple[int, int, str, list[tuple[int, int]]]:
    builder = build_message if not is_sale else build_sale_message
    msg = builder(product, GENDER)

    plinks = get_product_picture_links(product.id)
    pictures = []
    for idx, link in enumerate(plinks):
        pictures.append(InputMediaPhoto(link, caption=msg if idx == 0 else None, parse_mode="HTML"))
    pictures = pictures[:4]
    # message = await random.choice(bots).send_photo(chat_id, photo=photo_url, caption=msg, reply_markup=keyboard, parse_mode="MARKDOWN")
    try:
        messages = await random.choice(bots).send_media_group(CHAT_ID, pictures)
        if not is_sale: set_renew_flag(True)
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

async def renew_telegram_post(chat_id: int, msg_id: int, product: ProductInfo, prev_text: str, photo_infos: list[tuple[int, int]], is_sale: bool = False):
    builder = build_message if not is_sale else build_sale_message
    msg = builder(product, GENDER)
    link = get_product_picture_links(product.id)[0]
    photo = InputMediaPhoto(link, caption=msg, parse_mode="HTML")
    await random.choice(bots).edit_message_media(photo, chat_id=chat_id, message_id=msg_id)
    plinks = get_product_picture_links(product.id)
    for photo_info, plink in zip(photo_infos, plinks[1:]):
        pchat_id, pmsg_id = photo_info
        photo = InputMediaPhoto(plink)
        await random.choice(bots).edit_message_media(photo, chat_id=pchat_id, message_id=pmsg_id)
