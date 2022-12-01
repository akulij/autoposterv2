import datetime
from typing import Literal
from .db import ProductInfo
from . import storer as db_peewee
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def build_message(product: ProductInfo, gender: Literal["man"] | Literal["woman"]):
    description = ""
    description_max_len = 200
    if product.description:
        tail = "..." if len(product.description) > description_max_len else ""
        description = f"{product.description[:description_max_len].strip()}{tail}\n\n"
        # description = product.description
    tags = ""
    if product.tags:
        tags = product.tags
    parsed_sizes = ""
    if product.sizes:
        parsed_sizes = product.sizes
        if type(parsed_sizes) != str:
            sizes = product.sizes[gender]
            grouped_sizes = group_sizes(sizes)
            parsed_sizes = parse_sizes(grouped_sizes)
    post_format = db_peewee.get_post_format()
    url, order_url = build_keyboard(product, gender)
    if product.is_discount:
        new_price = product.price * (100 - product.discount_size) / 100
        date_now = datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y")
        msg = post_format.format(name=product.name, price=product.price, description=description, sizes=parsed_sizes, tags=tags, product_url=url, order_url=order_url, new_price=new_price, date=date_now)
    else:
        msg = post_format.format(name=product.name, price=product.price, description=description, sizes=parsed_sizes, tags=tags, product_url=url, order_url=order_url)
    # msg = (
    #         f"*{product.name}* - *{product.price} $*\n"
    #         f"\n"
    #         f"{description}\n"
    #         f"Размеры: {sizes}\n"
    #         f"{tags}"
    #         )
    return msg

def build_sale_message(product: ProductInfo, gender: Literal["man"] | Literal["woman"]):
    description = ""
    description_max_len = 200
    if product.description:
        tail = "..." if len(product.description) > description_max_len else ""
        description = f"{product.description[:description_max_len].strip()}{tail}\n\n"
        # description = product.description
    tags = ""
    if product.tags:
        tags = product.tags
    parsed_sizes = ""
    if product.sizes:
        parsed_sizes = product.sizes
        if type(parsed_sizes) != str:
            sizes = product.sizes[gender]
            grouped_sizes = group_sizes(sizes)
            parsed_sizes = parse_sizes(grouped_sizes)
    post_format = db_peewee.get_sale_post_format()
    new_price = product.price * (100 - product.discount_size) / 100
    date_now = datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y")
    url, order_url = build_keyboard(product, gender)
    msg = post_format.format(name=product.name, price=product.price, description=description, sizes=parsed_sizes, tags=tags, product_url=url, order_url=order_url, new_price=new_price, date=date_now)
    return msg

def build_keyboard(product: ProductInfo, gender: Literal["man"] | Literal["woman"]):
    keyboard = InlineKeyboardMarkup()
    man_url = f"https://www.sneakerhead.su/product/{product.hpu}"
    woman_url = f"https://www.sneakerhead.su/product/women/{product.hpu}"
    url = man_url if gender == "man" else woman_url
    keyboard.add(InlineKeyboardButton("Go to site", url=url))
    man_order_url = f"https://www.snkrs.su/checkouts/ocf5safdi0bypjlet01u_info_{product.id}"
    woman_order_url = f"https://www.snkrs.su/checkouts/ocf5safdi0bypjlet01u_infow_{product.id}"
    order_url = man_order_url if gender == "man" else woman_order_url
    keyboard.add(InlineKeyboardButton("Order", url=order_url))

    return url, order_url
    return keyboard

def group_sizes(sizes) -> dict[str, list[float]]:
    sizes_table = {
            "US": [min(sizes["US"]) if sizes["US"] else 1000., max(sizes["US"]) if sizes["US"] else -1000.],
            "UK": [min(sizes["UK"]) if sizes["UK"] else 1000., max(sizes["UK"]) if sizes["UK"] else -1000.],
            "EU": [min(sizes["EU"]) if sizes["EU"] else 1000., max(sizes["EU"]) if sizes["EU"] else -1000.],
            }
    return sizes_table

def parse_sizes(sizes_dict):
    ps = []
    for code, sizes in sizes_dict.items():
        if sizes[0] != 1000. and sizes[1] != -1000.:
            f = f"{code}{sizes[0]:.0f}-{sizes[1]:.0f}"
            ps.append(f)
    return ", ".join(ps)
