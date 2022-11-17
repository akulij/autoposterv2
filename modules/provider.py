from .types import ProductInfo
from .db import (
        get_product_info,
        get_db_product_ids,
        )
from .storer import (
        get_posted_product_ids,
        is_product_posted,
        add_post,
        )
from .poster import publish_to_telegram, renew_telegram_post


def get_new_products():
    posted_products = get_posted_product_ids()
    db_products = get_db_product_ids()
    new_product_ids = list(set(db_products) - set(posted_products))
    new_products = []
    for product_id in new_product_ids:
        product = get_product_info(product_id)
        # new_products.append(product)
        yield product

    # return new_products


def get_edit_products():
    pass


def get_sale_products():
    pass


def delete_sale_products():
    pass


async def make_post(product: ProductInfo):
    if not is_product_posted(product.id):
        chat_id, msg_id, photo_infos = await publish_to_telegram(product)
        add_post(product.id, chat_id, msg_id, photo_infos)
    else:
        chat_id, msg_id, post_text = get_product_post(product.id)
        await renew_telegram_post(chat_id, msg_id, product, post_text)


def make_sale_post(product: ProductInfo):
    pass
