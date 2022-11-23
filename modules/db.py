import re
from typing import Generator
import datetime

from sqlalchemy import create_engine
from sqlalchemy import select
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


def _test():
    q = select(Product).join(ProductFlags, Product.id == ProductFlags.id).where(ProductFlags.update_flag == 1)
    # q = select(ProductFlags).where(ProductFlags.update_flag == 1)
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
    q = select(Product.id).where((Product.active == 1), (Product.dSale_SN == 1))
    products = session.scalars(q).all()

    return products

def get_db_edit_product_ids() -> list[int]:
    # q = select(Product.id).where((Product.active == 1), (Product.dSale_SN == 1))
    q = select(Product.id).join(ProductFlags, Product.id == ProductFlags.id).where((ProductFlags.update_flag == 1), (Product.active == 1))
    # q = select(ProductFlags.id).where(ProductFlags.update_flag == 1)
    products = session.scalars(q).all()

    return products
# print(get_db_edit_product_ids())

def get_product_picture_links(product_id: int):
    return db_utils.get_product_picture_links(session, product_id)
