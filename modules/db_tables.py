from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, DateTime


Base = declarative_base()


class Product(Base):
    __tablename__ = "boxed_prod_content"

    id = Column(Integer, primary_key=True)
    active = Column(Integer)
    name = Column(String)
    price = Column(Float)
    Text = Column(String)
    id_catalog = Column(Integer)
    id_category = Column(Integer)
    size = Column(VARCHAR)
    tags = Column(String)
    gM = Column(Integer)
    gW = Column(Integer)
    date_add = Column(DateTime)
    date_upd = Column(DateTime)

    dSale_SN = Column(Integer)
    discount_SN = Column(Integer)
    dSaleDateEnd_SN =Column(DateTime)
    
    def __str__(self):
        return str(self.__dict__)

class Uri(Base):
    __tablename__ = "Uri_setting"

    id = Column(Integer, primary_key=True)
    type = Column(VARCHAR)
    id_type = Column(Integer)
    hpu = Column(VARCHAR)

class Category(Base):
    __tablename__ = "category"

    id_category = Column(Integer, primary_key=True)
    product_razmer = Column(Integer)

class SizeContent(Base):
    __tablename__ = "SizeContent"

    id = Column(Integer, primary_key=True)
    id_category = Column(Integer)
    US = Column(VARCHAR)
    USw = Column(VARCHAR)
    UK = Column(VARCHAR)
    EU = Column(VARCHAR)
    name = Column(VARCHAR)
    active = Column(Integer)
    Gm = Column(Integer)
    Gw = Column(Integer)

class ProductPicture(Base):
    __tablename__ = "boxed_prod_img"

    id = Column(Integer, primary_key=True)
    img = Column(VARCHAR)
    sort = Column(Integer)
    product_id = Column(Integer)

class ProductFlags(Base):
    __tablename__ = "boxed_prod"

    id = Column(Integer, primary_key=True)
    update_flag = Column(Integer)
    update_flag_ru = Column(Integer)
