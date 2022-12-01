import time
import asyncio
from modules.provider import (
        get_new_products,
        get_edit_products,
        get_edit_sale_products,
        get_sale_products,
        delete_sale_products,
        make_post,
        make_sale_post,
        make_prepost,
        delete_preposts,
        get_removed_sale_product_ids,
        delete_sale_post,
        )
from modules.storer import (
        get_renew_flag,
        set_renew_flag,
        )


async def main():
    while True:
        print("posting new products...")
        for product in get_new_products():
            set_renew_flag(True)
            print(product)
            await make_post(product)
            # time.sleep(2)
            print(f"made post of {product}")
        print("editing products...")
        for product in get_edit_products():
            # set_renew_flag(True)
            await make_post(product)
            print(f"edited product {product}")

        if get_renew_flag():
            print("deleting unneeded")
            await delete_sale_products()
            await delete_preposts()
            set_renew_flag(False)
            await make_prepost()

        print("making sale posts")
        for product_id in get_removed_sale_product_ids():
            await delete_sale_post(product_id)
        for product in get_edit_sale_products():
            await make_sale_post(product)
        for product in get_sale_products():
            await make_sale_post(product)

        await asyncio.sleep(10)
        print("end of")


if __name__ == "__main__":
    asyncio.run(main())
