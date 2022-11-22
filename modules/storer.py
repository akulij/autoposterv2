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
    db.create_tables([User, PostId, PostFormat, Admin, SalePostId, SalePostFormat, RenewPosts, PrepostInfo, Prepost, NoPhotoSalePostId, RefreshAll])


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


def is_product_posted(product_id: int):
    return PostId.select().where(PostId.product_id == product_id).exists()


def add_post(product_id: int, chat_id: int, message_id: int, message_text: str, photo_infos: list):
    PostId.create(product_id=product_id, chat_id=chat_id, message_id=message_id)
    for info in photo_infos:
        raise NotImplemented

def set_renew_flag(flag: bool):
    if RenewPosts.select().exists():
        RenewPosts.update(flag=flag).execute()
    else:
        RenewPosts.create(flag=flag)
