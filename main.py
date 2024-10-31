from products import Products
from web_driver_handler import WebDriverHandler

URL: str = "https://orteil.dashnet.org/cookieclicker/"

driver = WebDriverHandler(URL)

products = Products(driver)

cookie_count: int = 0

while True:
    cookie_count = driver.get_cookie_count()

    products.check_if_next_product_unlocked()

    price = products.buy_product(cookie_count)
    cookie_count -= price

    for _ in range(100):
        driver.click_cookie()

    if not (upgrade := driver.get_current_upgrades()):
        continue

    price = driver.buy_upgrade(upgrade["price"], cookie_count, upgrade["id"])
    cookie_count -= price
