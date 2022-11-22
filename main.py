import asyncio
from modules.provider import (
        get_new_products,
        get_edit_products,
        get_sale_products,
        delete_sale_products,
        make_post,
        make_sale_post,
        )


async def main():
    while True:
        is_new_product = False
        for product in get_new_products():
            print(product)
            await make_post(product)
        for product in get_edit_products():
            is_new_product = True
            await make_post(product)
        if is_new_product:
            delete_sale_products()
        for product in get_sale_products():
            await make_sale_post(product)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
