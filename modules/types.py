from pydantic import BaseModel as Pydantic


class ProductInfo(Pydantic):
    id: int
    is_for_man: bool
    is_for_woman: bool
    name: str
    price: float
    description: str | None
    sizes: str | dict | None
    photo_url: str
    # site_link: str
    # order_link: str
    hpu: str | None
    is_updated: bool
    tags: str | None
    is_discount: bool
    discount_size: int

