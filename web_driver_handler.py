from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


class WebDriverHandler:
    def __init__(self, URL: str) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get(URL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.click_on_cookie_stuff()
        self.click_language()

        self.cookie_element = self.get_big_cookie()

        for _ in range(20):
            self.cookie_element.click()

    def click_cookie(self) -> None:
        sleep(0.1)
        self.cookie_element.click()

    def click_on_cookie_stuff(self) -> None:
        self.driver.find_element(By.CLASS_NAME, "fc-button-label").click()

    def click_language(self) -> None:
        self.driver.find_element(By.ID, "langSelect-EN").click()

    def get_big_cookie(self) -> webdriver.remote.webelement.WebElement:
        return self.driver.find_element(By.ID, "bigCookie")

    def get_buildings(self) -> list[dict]:
        return self.driver.execute_script(
            """
            return Object.values(Game.ObjectsById).map(function(building) {
                return {
                    id: building.id,
                    name: building.name,
                    price: building.price,
                    cps: building.cps(this) || building.storedCps,
                    amount: building.amount,
                    locked: building.locked
                };
            });
        """
        )

    def get_new_price_for_building(self, building_id: int) -> int:
        return self.driver.execute_script(
            f"return Game.ObjectsById[{building_id}].getPrice();"
        )

    def find_product(self, product_id: int) -> webdriver.remote.webelement.WebElement:
        return self.driver.find_element(By.ID, f"product{product_id}")

    def get_cookie_count(self) -> int:
        return int(self.driver.execute_script("return Game.cookies;"))

    def get_is_avaiable(self, product_id: int) -> bool:
        return not self.driver.execute_script(
            f"return Game.ObjectsById[{product_id}].locked;"
        )
