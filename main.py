import asyncio
from modules.provider import (
        get_new_products,
        get_edit_products,
        get_sale_products,
        delete_sale_products,
        make_post,
        make_sale_post,
        make_prepost,
        delete_preposts,
        )
from modules.storer import (
        get_renew_flag,
        set_renew_flag,
        )


async def main():
    while True:
        for product in get_new_products():
            set_renew_flag(True)
            print(product)
            await make_post(product)
        for product in get_edit_products():
            set_renew_flag(True)
            await make_post(product)
        if get_renew_flag():
            await delete_sale_products()
            await delete_preposts()
            set_renew_flag(False)
        await make_prepost()
        for product in get_sale_products():
            await make_sale_post(product)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
