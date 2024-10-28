import time

from product import Product
from products import Products
from web_driver_handler import *

URL = "https://orteil.dashnet.org/cookieclicker/"

webDriverHandler = WebDriverHandler(URL)
products = Products()
cookie_count = 0

for product_item in webDriverHandler.get_buildings():
    product = Product(
        id=product_item["id"],
        name=product_item["name"],
        price=product_item["price"],
        cps=product_item["cps"],
        web_element=webDriverHandler.find_product(product_item["id"]),
        is_avaiable=not product_item["locked"],
    )

    products.add_product(product)

next_to_buy = products.best_to_buy()
count = 0
next_avaiable_product_index = 1
cookie_count = webDriverHandler.get_cookie_count()

while True:
    if count % 100 == 0:
        if webDriverHandler.get_is_avaiable(next_avaiable_product_index):
            product = products.products_list[next_avaiable_product_index]

            product.is_avaiable = True
            next_to_buy = products.best_to_buy()

            next_avaiable_product_index += 1
        count = 0

        cookie_count = webDriverHandler.get_cookie_count()
        print("cookie count:", cookie_count)

    webDriverHandler.cookie_element.click()

    if cookie_count >= next_to_buy.price:
        next_to_buy.web_element.click()
        next_to_buy.price = webDriverHandler.get_new_price_for_building(next_to_buy.id)

        cookie_count -= next_to_buy.price

        next_to_buy = products.best_to_buy()

    count += 1
