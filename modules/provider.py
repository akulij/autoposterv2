from .types import ProductInfo
from .db import (
        get_product_info,
        get_db_product_ids,
        get_db_edit_product_ids,
        get_db_sale_product_ids,
        set_edited,
        )
from .storer import (
        get_posted_product_ids,
        is_product_posted,
        is_sale_product_posted,
        add_post,
        add_sale_post,
        get_product_post,
        get_sale_product_post,
        get_posted_sale_product_ids,
        delete_sale_post as db_delete_sale_post,
        get_nophoto_sale_posts,
        get_sale_messages,
        get_prepost_info,
        create_prepost,
        get_preposts,
        delete_prepost,
        get_sale_product_message,
        get_db_unmatching_date_product_ids,
        )
from .poster import (publish_to_telegram,
        renew_telegram_post,
        delete_telegram_message,
        publish_prepost_telegram
        )


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

def get_removed_sale_product_ids():
    posted_products = get_posted_product_ids()
    db_products = get_db_product_ids()
    removed_ids = list(set(posted_products) - set(db_products))

    return removed_ids


def get_edit_products():
    edit_product_ids = get_db_edit_product_ids()
    for product_id in edit_product_ids:
        product = get_product_info(product_id)
        yield product

def get_edit_sale_products():
    edit_product_ids = get_db_edit_product_ids()
    unmatching_date_ids = get_db_unmatching_date_product_ids()
    product_ids = set(edit_product_ids)
    product_ids.union(unmatching_date_ids)
    for product_id in product_ids:
        product = get_product_info(product_id)
        yield product


def get_sale_products():
    posted_products = get_posted_sale_product_ids()
    db_products = get_db_sale_product_ids()
    new_sale_product_ids = list(set(db_products) - set(posted_products))
    for product_id in new_sale_product_ids:
        product = get_product_info(product_id)
        # new_products.append(product)
        yield product

async def delete_sale_post(product_id: int):
    for chat_id, msg_id in get_sale_product_message(product_id):
        try:
            await delete_telegram_message(chat_id, msg_id)
        except:
            pass
        db_delete_sale_post(product_id)
        for chat_id, msg_id in get_nophoto_sale_posts(product_id, chat_id):
            try:
                await delete_telegram_message(chat_id, msg_id)
            except:
                pass

async def delete_sale_products():
    for product_id, _, _ in get_sale_messages():
        await delete_sale_post(product_id)


async def make_post(product: ProductInfo):
    if not is_product_posted(product.id):
        chat_id, msg_id, msg_text, photo_infos = await publish_to_telegram(product)
        add_post(product.id, chat_id, msg_id, msg_text, photo_infos)
    else:
        chat_id, msg_id, post_text, photo_infos = get_product_post(product.id)
        await renew_telegram_post(chat_id, msg_id, product, post_text, photo_infos)
        set_edited(product.id)


async def make_sale_post(product: ProductInfo):
    if not is_sale_product_posted(product.id):
        chat_id, msg_id, msg_text, photo_infos = await publish_to_telegram(product, is_sale=True)
        add_sale_post(product.id, chat_id, msg_id, msg_text, photo_infos)
    else:
        chat_id, msg_id, post_text, photo_infos = get_sale_product_post(product.id)
        await renew_telegram_post(chat_id, msg_id, product, post_text, photo_infos, is_sale=True)

async def make_prepost():
    prepost = get_prepost_info()
    chat_id, msg_id = await publish_prepost_telegram(prepost)
    create_prepost(chat_id, msg_id)

async def delete_preposts():
    for chat_id, msg_id in get_preposts():
        await delete_telegram_message(chat_id, msg_id)
        delete_prepost(chat_id, msg_id)
