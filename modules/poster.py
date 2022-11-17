from .types import ProductInfo

async def publish_to_telegram(product: ProductInfo):
    pass

async def renew_telegram_post(chat_id: int, msg_id: int, product: ProductInfo, prev_text: str):
    pass
