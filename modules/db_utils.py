import re

from sqlalchemy import select

from .types import ProductInfo
from .db_tables import *


def get_product_data(session, item_id: int) -> Product:
    # print(dir(session.query(Product).filter(Product.id.is_(item_id))))
    # session.query(Product).first()
    return session.query(Product).filter(Product.id == (item_id)).first()

def get_product_info(session, item_id: int, session_uri) -> ProductInfo:
    product = get_product_data(session, item_id)
    name = product.name
    price = product.price
    sizes = get_product_sizes(session, item_id)
    tags = product.tags
    photo_url = f"https://www.snkrs.su/img/product/product_{item_id}/img.jpg"
    try:
        hpu = get_hpu(session_uri, item_id)
    except AttributeError:
        print(f"product without hpu: {item_id}")
        hpu = None
    # site_link = f"https://www.snkrs.su/product/{hpu}"
    # order_link = f"https://www.snkrs.su/checkouts/ocf5safdi0bypjlet01u_info_{item_id}"
    description: str = str(product.Text)[:200] if product.Text else ""
    is_for_man = True if product.gM else False
    is_for_woman = True if product.gW else False
    is_discount = True if product.dSale_SN else False
    discount_size = product.discount_SN

    # TODO: Unimplemented
    is_updated = False

    pi = ProductInfo(
            id=item_id,
            is_for_man=is_for_man,
            is_for_woman=is_for_woman,
            name=str(name),
            price=price,
            description=description,
            sizes=sizes,
            photo_url=photo_url,
            # site_link=site_link,
            # order_link=order_link,
            hpu=hpu,
            is_updated=is_updated,
            tags=str(tags),
            is_discount=is_discount,
            discount_size=int(str(discount_size)),
            )
    return pi

def get_hpu(session_uri, item_id: int):
    return session_uri.query(Uri).filter(Uri.type == "product", Uri.id_type == item_id).first().hpu


def prepare_size(size: str) -> float:
    r = re.compile(r"([0-9]+\.?[0-9]*)")

    return float(r.search(size)[1])

def get_product_sizes(session, item_id: int):
    sizes_arr = {
            "man": {
                "US": [],
                "UK": [],
                "EU": [],
                },
            "woman": {
                "US": [],
                "UK": [],
                "EU": [],
                },
            }
    product = get_product_data(session, item_id)
    if product.id_catalog == 148:
        return str(product.size)
    else:
        size = session.query(Category).filter(Category.id_category == product.id_category).first().product_razmer
        q = select(SizeContent).where(SizeContent.id_category == size, SizeContent.active == 1)
        # US USw UK EU
        for size in session.scalars(q):
            if size.Gw:
                if size.US:
                    sizes_arr["woman"]["US"].append(prepare_size(size.US))
                if size.USw:
                    sizes_arr["woman"]["US"].append(prepare_size(size.USw))
                if size.UK:
                    sizes_arr["woman"]["UK"].append(prepare_size(size.UK))
                if size.EU:
                    sizes_arr["woman"]["EU"].append(prepare_size(size.EU))
            if size.Gm:
                if size.US:
                    sizes_arr["man"]["US"].append(prepare_size(size.US))
                if size.UK:
                    sizes_arr["man"]["UK"].append(prepare_size(size.UK))
                if size.EU:
                    sizes_arr["man"]["EU"].append(prepare_size(size.EU))
        return sizes_arr

def is_product_active(session, item_id: int):
    return bool(session.query(Product).filter(Product.id == item_id).first().active)

def get_product_picture_links(session, product_id: int):
    q = select(ProductPicture).where(ProductPicture.product_id == product_id).order_by(ProductPicture.sort)
    pictures = []
    for picture in session.scalars(q):
        picture_link = f"https://www.snkrs.su/img/product/product_{product_id}/{picture.img}"
        pictures.append(picture_link)

    return pictures

def is_product_sale(session, product_id: int) -> bool:
    try:
        return bool(session.query(Product).filter(Product.id == product_id).first().dSale_SN)
    except:
        return False
