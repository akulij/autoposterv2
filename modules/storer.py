from peewee import (
    SqliteDatabase,
    Model,
)

db = SqliteDatabase("application.db")


class BaseModel(Model):
    class Meta:
        database = db

from .storer_tables import *


def migrate():
    db.create_tables([User, PostId, PostFormat, Admin, SalePostId, SalePostFormat, RenewPosts, PrepostInfo, Prepost, NoPhotoSalePostId, RefreshAll, PostPhoto, SalePostPhoto])


def test_get_posted_product_ids():
    posted_products = get_posted_product_ids()
    assert type(posted_products) == list
    for product_id in posted_products:
        assert type(product_id) == int
        

def get_posted_product_ids() -> list[int]:
    products = PostId.select()
    product_ids = []
    for product in products:
        product_ids.append(product.product_id)

    return product_ids


def get_posted_sale_product_ids() -> list[int]:
    products = SalePostId.select()
    product_ids = []
    for product in products:
        product_ids.append(product.product_id)

    return product_ids

def is_product_posted(product_id: int):
    return PostId.select().where(PostId.product_id == product_id).exists()


def add_post(product_id: int, chat_id: int, message_id: int, message_text: str, photo_infos: list[tuple[int, int]]):
    PostId.create(product_id=product_id, chat_id=chat_id, message_id=message_id)
    for info in photo_infos:
        PostPhoto.create(product_id=product_id, chat_id=info[0], message_id=info[1])

def add_sale_post(product_id: int, chat_id: int, message_id: int, message_text: str, photo_infos: list[tuple[int, int]]):
    SalePostId.create(product_id=product_id, chat_id=chat_id, message_id=message_id)
    for info in photo_infos:
        SalePostPhoto.create(product_id=product_id, chat_id=info[0], message_id=info[1])

def get_sale_messages():
    msgs = []
    for msg in SalePostId.select():
        msgs.append((msg.product_id, msg.chat_id, msg.message_id))

    return msgs

def get_nophoto_sale_posts(product_id: int, chat_id: int) -> list[tuple[int, int]]:
    q = SalePostPhoto.select().where((SalePostPhoto.product_id==product_id), (SalePostPhoto.chat_id == chat_id))
    posts = []
    for post in q:
        posts.append((post.chat_id, post.message_id))
    return posts

def delete_sale_post(product_id: int):
    SalePostId.delete().where(SalePostId.product_id == product_id).execute()

def get_product_post(product_id: int) -> tuple[int, int, str, list[tuple[int, int]]]:
    """
    return: chat_id, message_id, post_text, photo_infos
    """
    post = PostId.select().where(PostId.product_id==product_id).get()
    q = PostPhoto.select().where(PostPhoto.product_id==product_id)
    photo_infos = []
    for photo in q:
        photo_infos.append((photo.chat_id, photo.msg_id))
    return post.chat_id, post.message_id, "", photo_infos

def get_sale_product_post(product_id: int) -> tuple[int, int, str, list[tuple[int, int]]]:
    """
    return: chat_id, message_id, post_text, photo_infos
    """
    post = SalePostId.select().where(SalePostId.product_id==product_id).get()
    q = SalePostPhoto.select().where(SalePostPhoto.product_id==product_id)
    photo_infos = []
    for photo in q:
        photo_infos.append((photo.chat_id, photo.msg_id))
    return post.chat_id, post.message_id, "", photo_infos


def set_renew_flag(flag: bool):
    if RenewPosts.select().exists():
        RenewPosts.update(flag=flag).execute()
    else:
        RenewPosts.create(flag=flag)

def get_renew_flag() -> bool:
    if RenewPosts.select().exists():
        return RenewPosts.select().get().flag
    else:
        return False

def get_prepost_info():
    return PrepostInfo.select().get()

def set_prepost_info(caption: str | None = None, photo: str | None = None):
    if PrepostInfo.select().exists():
        if caption:
            PrepostInfo.update(caption=caption).execute()
        if photo:
            PrepostInfo.update(photo=photo).execute()
    else:
        PrepostInfo.create(photo=photo, caption=caption)

def create_prepost(chat_id: int, message_id: int):
    Prepost.create(chat_id=chat_id, message_id=message_id)

def get_preposts():
    post_query = Prepost.select()
    posts = []
    for post in post_query:
        posts.append((post.chat_id, post.message_id))

    return posts

def delete_prepost(chat_id: int, message_id: int):
    Prepost.delete().where(Prepost.chat_id == chat_id, Prepost.message_id == message_id).execute()

