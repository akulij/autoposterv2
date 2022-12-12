import traceback
import os
import random
import time
from typing import Literal

from aiogram.types import InputMediaPhoto, InputFile
from aiogram import Bot

from .types import ProductInfo
from .db import get_product_picture_links
from .builder import build_message, build_sale_message, build_prepost
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
        "5969901906:AAG0VkTCjn91oLNmcQMZURXIsPeisiMb7Sw",
        "5903197168:AAFUCw8k7pmX9z9N5HKCUJzoeOY3WmyM5vM",
        "5921124241:AAHA7phI42KUK2nYwmhqnAlNPRaRFfUmIyI",
        ]
bots: list[Bot] = []
for token in TOKENS:
    bots.append(Bot(token))

def generator(l):
    idx = 0
    while True:
        yield l[idx%len(l)]
        idx += 1

bot = generator(bots)

async def publish_to_telegram(product: ProductInfo, is_sale: bool = False) -> tuple[int, int, str, list[tuple[int, int]]]:
    builder = build_message if not is_sale else build_sale_message
    msg = builder(product, GENDER)

    plinks = get_product_picture_links(product.id)
    pictures = []
    print(msg)
    for idx, link in enumerate(plinks):
        print(link)
        pictures.append(InputMediaPhoto(link, caption=msg if idx == 0 else None, parse_mode="HTML"))
    pictures = pictures[:4]
    # message = await next(bot).send_photo(chat_id, photo=photo_url, caption=msg, reply_markup=keyboard, parse_mode="MARKDOWN")
    # if True:
    while True:
        try:
            poster = next(bot)
            if pictures:
                messages = await poster.send_media_group(CHAT_ID, pictures)
            else:
                return [None] * 4
            if not is_sale: set_renew_flag(True)
            # time.sleep(4)
            caption_message = messages[0]
            photo_messages = messages[1:]
            chat_id = caption_message.chat.id
            msg_id = caption_message.message_id
            photo_infos = []
            for photo_msg in photo_messages:
                photo_infos.append((photo_msg.chat.id, photo_msg.message_id))

            return chat_id, msg_id, msg, photo_infos
        except Exception as e:
            # await bots[0].send_message(958170391, f"Catched Exception: {e}\nTraceback: {traceback.format_exc()}")
            print(e)
            print("sleeping for 10 seconds...")
            if "#" in str(e):
                parts = str(e).split()
                for part in parts:
                    if part[0] == "#":
                        n = int(part[1:])
                        print(n)
                        print(len(pictures))
                        pictures.pop(n-1)
            time.sleep(10)

async def renew_telegram_post(chat_id: int, msg_id: int, product: ProductInfo, prev_text: str, photo_infos: list[tuple[int, int]], is_sale: bool = False):
    builder = build_message if not is_sale else build_sale_message
    msg = builder(product, GENDER)
    link = get_product_picture_links(product.id)[0]
    photo = InputMediaPhoto(link, caption=msg, parse_mode="HTML")
    try:
        print(f"trying to edit product {product.id}")
        await next(bot).edit_message_media(photo, chat_id=chat_id, message_id=msg_id)
    except:
        print(f"product {product.id} not edited")
        pass
    plinks = get_product_picture_links(product.id)
    for photo_info, plink in zip(photo_infos, plinks[1:]):
        pchat_id, pmsg_id = photo_info
        photo = InputMediaPhoto(plink)
        try:
            await next(bot).edit_message_media(photo, chat_id=pchat_id, message_id=pmsg_id)
        except:
            pass

async def delete_telegram_message(chat_id: int, msg_id: int):
    await next(bot).delete_message(chat_id, msg_id)

async def publish_prepost_telegram(prepost):
    caption = build_prepost(prepost.caption)
    if prepost.photo:
        if prepost.is_photo_file:
            msg = await next(bot).send_photo(CHAT_ID, InputFile(prepost.photo), caption, parse_mode="HTML")
        else:
            msg = await next(bot).send_photo(CHAT_ID, prepost.photo, caption, parse_mode="HTML")
    else:
        msg = await next(bot).send_message(CHAT_ID, caption, parse_mode="HTML")

    return (msg.chat.id, msg.message_id)
