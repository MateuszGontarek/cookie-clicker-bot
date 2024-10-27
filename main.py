import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException

class Product:
    def __init__(self, id: int, name: str, price: float, ratio: float, web_element) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.ratio = ratio
        self.web_element = web_element

    def calculate_ratio_per_price(self):
        return self.ratio / self.price

class Products:
    def __init__(self) -> None:
        self.products: list[Product] = []

    def key_function(self, product: Product):
        return product.calculate_ratio_per_price()
    
    def best_to_buy(self) -> Product:
        self.products = sorted(self.products_list, key=self.key_function)

        return self.products[-1]
    
    def add_product(self, product: Product) -> None:
        self.products.append(product)


def click_on_cookie_stuff(driver: webdriver) -> None:
    driver.find_element(By.CLASS_NAME, "fc-button-label").click()

def click_language(driver: webdriver) -> None:
    driver.find_element(By.ID, "langSelect-EN").click()
    

def get_big_cookie(driver: webdriver):
    return driver.find_element(By.ID, "bigCookie")
    

URL = "https://orteil.dashnet.org/cookieclicker/"
driver = webdriver.Chrome()

driver.get(URL)
driver.maximize_window()
driver.implicitly_wait(10)

click_on_cookie_stuff(driver)
click_language(driver)

cookie_element = get_big_cookie(driver)
cookie_count = 0
next_product_to_buy = None

products = Products()

for product_item in driver.find_elements(By.CLASS_NAME, "product"):
    product_id = product_item.get_attribute("id")

    product_content = product_item.find_element(By.CLASS_NAME, "content")
    
    product_name = product_content.find_element(By.CLASS_NAME, "title").text
    
    product_price = product_content.find_element(By.CLASS_NAME, "price").text

    product_price = product_price.replace(",", "").split()

    print(product_price)
    price = float(product_price[0])
    
    if len(product_price) > 1:
        match product_price[1]:
            case "million":
                product_price = price * 10 ** 6
            case "billion":
                product_price = price * 10 ** 9
            case "trillion":
                product_price = price * 10 ** 12
            case "quadrillion":
                product_price = price * 10 ** 15
            case "quintillion":
                product_price = price * 10 ** 18
            case "sextillion":
                product_price = price * 10 ** 21
            case "septillion":
                product_price = price * 10 ** 24
    else:
        product_price = price

    product_ratio = 1
    
    product = Product(product_id, product_name, product_price, product_ratio, product_item)

    products.add_product(product)


while True:
    cookie_count = driver.title.split()[0]
    cookie_element.click()

    time.sleep(0.1)
    