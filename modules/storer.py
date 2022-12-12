from datetime import datetime, timedelta
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

def is_sale_product_posted(product_id: int):
    return SalePostId.select().where(SalePostId.product_id == product_id).exists()


def add_post(product_id: int, chat_id: int, message_id: int, message_text: str, photo_infos: list[tuple[int, int]]):
    PostId.create(product_id=product_id, chat_id=chat_id, message_id=message_id)
    for info in photo_infos:
        PostPhoto.create(product_id=product_id, chat_id=info[0], message_id=info[1])

def add_sale_post(product_id: int, chat_id: int, message_id: int, message_text: str, photo_infos: list[tuple[int, int]]):
    date = datetime.strftime(datetime.now(), "%d-%m-%Y")
    SalePostId.create(product_id=product_id, chat_id=chat_id, message_id=message_id, date_posted=date)
    for info in photo_infos:
        SalePostPhoto.create(product_id=product_id, chat_id=info[0], message_id=info[1])

def get_sale_messages():
    msgs = []
    for msg in SalePostId.select():
        msgs.append((msg.product_id, msg.chat_id, msg.message_id))

    return msgs

def get_sale_product_message(product_id: int) -> list[tuple[int, int]]:
    q = SalePostId.select().where((SalePostId.product_id==product_id))
    posts = []
    for post in q:
        posts.append((post.chat_id, post.message_id))
    return posts

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
        photo_infos.append((photo.chat_id, photo.message_id))
    return post.chat_id, post.message_id, "", photo_infos

def get_sale_product_post(product_id: int) -> tuple[int, int, str, list[tuple[int, int]]]:
    """
    return: chat_id, message_id, post_text, photo_infos
    """
    post = SalePostId.select().where(SalePostId.product_id==product_id).get()
    q = SalePostPhoto.select().where(SalePostPhoto.product_id==product_id)
    photo_infos = []
    for photo in q:
        photo_infos.append((photo.chat_id, photo.message_id))
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

# def get_prepost_info() -> PrepostInfo:
def get_prepost_info():
    return PrepostInfo.select().get()

def set_prepost_info(caption: str | None = None, photo: str | None = None, is_photo_file: bool = False):
    if PrepostInfo.select().exists():
        if caption:
            PrepostInfo.update(caption=caption).execute()
        if photo:
            PrepostInfo.update(photo=photo, is_photo_file=is_photo_file).execute()
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

def get_post_format() -> str:
    return PostFormat.select().get().format_text

def get_sale_post_format() -> str:
    return SalePostFormat.select().get().format_text

def set_post_format(format_text: str):
    PostFormat.delete().execute()
    PostFormat.create(format_text=format_text)

def set_sale_post_format(format_text: str):
    SalePostFormat.delete().execute()
    SalePostFormat.create(format_text=format_text)

def _add_user_unsafe(user_id: int):
    User.create(
        id=user_id,
        state="",
    )

def is_user_exists(user_id: int) -> bool:
    is_exists = User.select().where(User.id == user_id).exists()
    return is_exists

def add_user(user_id: int):
    if not is_user_exists(user_id):
        _add_user_unsafe(user_id)

def new_user(user_id: int):
    is_new_user = is_user_exists(user_id)
    add_user(user_id)
    return is_new_user

def add_admin(user_id: int):
    Admin.create(user_id=user_id)

def is_user_admin(user_id: int):
    return Admin.select().where(Admin.user_id ==  user_id).exists()

def set_user_state(user_id: int, state: str):
    User.update(state=state).where(User.id == user_id).execute()

def get_user_state(user_id: int) -> str:
    user = User.select().where(User.id == user_id).get()
    return user.state

def is_sale_post_date_actual(product_id: int, chat_id: int):
    # , (SalePostId.date_posted == datetime.now().date)
    try:
        post = SalePostId.select().where((SalePostId.product_id==product_id), (SalePostId.chat_id == chat_id)).get()
    except:
        return False
    if not post:
        return False
    else:
        date = datetime.now() - timedelta(hours=1)
        date_posted = datetime.strptime(post.date_posted, "%Y-%m-%d")
        return all([
            date_posted.day == date.day,
            date_posted.month == date.month,
            date_posted.year == date.year,
            ])

def get_db_unmatching_date_product_ids():
    products = SalePostId.select()
    for product in products:
        if not is_sale_post_date_actual(product.product_id, product.chat_id):
            yield product.product_id

def get_messages_desc():
    messages = PostId.select().order_by(PostId.message_id.desc())
    msg_list = []
    for msg in messages:
        msg_list.append(msg)

    return msg_list
