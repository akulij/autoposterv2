import os
import re
from typing import Literal
from string import ascii_uppercase, digits
from random import choice
from typing import Generator
import datetime

from sqlalchemy import create_engine
from sqlalchemy import select, update, exists, insert
from sqlalchemy.orm import sessionmaker

from .types import ProductInfo
from .db_tables import *
from . import db_utils

engine = create_engine("mysql+mysqldb://akulijdev:rerfhtre@178.32.58.161:3306/yeezydirect?charset=utf8mb4")
Session = sessionmaker(bind=engine)
session = Session()

engine_uri = create_engine("mysql+mysqldb://akulijdev:rerfhtre@178.32.58.161:3306/snkrs?charset=utf8mb4")
SessionUri = sessionmaker(bind=engine_uri)
session_uri = SessionUri()

from dotenv import load_dotenv

load_dotenv()
POSSIBLE_CHARS = ascii_uppercase + digits
GENDER: Literal["man", "woman"] = os.getenv("GENDER")
assert GENDER in ["man", "woman"]
update_flag = ProductFlags.update_flag_man_ru if GENDER == "man" else ProductFlags.update_flag_woman_ru

def _test():
    q = select(Product).join(ProductFlags, Product.id == ProductFlags.id).where(ProductFlags.update_flag_ru == 1)
    # q = select(ProductFlags).where(ProductFlags.update_flag_ru == 1)
    print(dir(session.scalars(q)))
    print(session.scalars(q).all())
    for product in session.scalars(q):
        print(product)

def get_product_info(product_id: int) -> ProductInfo:
    return db_utils.get_product_info(session, product_id, session_uri)

def get_db_product_ids() -> list[int]:
    q = select(Product.id).where(Product.active == 1)
    products = session.scalars(q).all()

    return products

def get_db_sale_product_ids() -> list[int]:
    q = select(Product.id).where((Product.active == 1), (Product.dSale_SH == 1))
    products = session.scalars(q).all()

    return products

def get_db_edit_product_ids() -> list[int]:
    q = select(Product.id).join(ProductFlags, Product.id == ProductFlags.id).where((update_flag == 1), (Product.active == 1))
    products = session.scalars(q).all()

    return products
print(get_db_edit_product_ids())

def set_refresh_all(flag: bool):
    if GENDER == "man":
        q = update(ProductFlags).where().values(update_flag_man_ru = int(flag))
    else:
        q = update(ProductFlags).where().values(update_flag_woman_ru = int(flag))
    session.execute(q)
    session.commit()

def set_edited(product_id: int):
    if GENDER == "man":
        q = update(ProductFlags).where(ProductFlags.id == product_id).values(update_flag_man_ru = 0)
    else:
        q = update(ProductFlags).where(ProductFlags.id == product_id).values(update_flag_woman_ru = 0)
    session.execute(q)
    session.commit()

def get_product_picture_links(product_id: int):
    return db_utils.get_product_picture_links(session, product_id)

def is_promo_exists(user_id: int) -> bool:
    q = exists().where(Promos.telegram_user_id == user_id)
    return session_uri.query(q).scalar()

def generate_promo():
    chars = (choice(POSSIBLE_CHARS) for _ in range(10))
    return "".join(chars)

def create_promo(user_id: int) -> str:
    promo = generate_promo()
    q = insert(Promos).values(promo=promo, telegram_user_id=user_id)
    session_uri.execute(q)
    session_uri.commit()
    return promo

def get_promo(user_id: int) -> str:
    if not is_promo_exists(user_id):
        promo = create_promo(user_id)
        return promo
    else:
        promo = (
                session_uri.query(Promos)
                .filter(Promos.telegram_user_id == user_id)
                .first().promo
                )
        return promo
