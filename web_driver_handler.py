from selenium import webdriver
from selenium.webdriver.common.by import By


class WebDriverHandler:
    def __init__(self, URL: str) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get(URL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)

        self.click_on_cookie_stuff()
        self.click_language()

        self.cookie_element = self.get_big_cookie()
        for _ in range(20):
            self.click_cookie()

    def click_cookie(self) -> None:
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

    def buy_upgrade(self, price: int, cookie_count: int, upgrade_id: int) -> int:
        if cookie_count < price:
            return 0

        self.driver.execute_script(f"Game.UpgradesById[{upgrade_id}].buy();")
        return price

    def get_new_price_for_building(self, building_id: int) -> int:
        return self.driver.execute_script(
            f"return Game.ObjectsById[{building_id}].getPrice();"
        )

    def get_cps_for_building(self, building_id: int) -> int:
        return self.driver.execute_script(
            f"return Game.ObjectsById[{building_id}].cps(this);"
        )

    def find_product(self, product_id: int) -> webdriver.remote.webelement.WebElement:
        return self.driver.find_element(By.ID, f"product{product_id}")

    def find_upgrade(self, upgrade_id: int) -> webdriver.remote.webelement.WebElement:
        return self.driver.find_element(By.ID, f"upgrade{upgrade_id}")

    def get_cookie_count(self) -> int:
        return int(self.driver.execute_script("return Game.cookies;"))

    def get_product_unlocked(self, product_id: int) -> bool:
        return not self.driver.execute_script(
            f"return Game.ObjectsById[{product_id}].locked;"
        )

    def get_current_upgrades(self) -> dict | None:
        upgrades = self.driver.execute_script(
            """
            return Game.UpgradesInStore.map(function(upgrade) {
                return {
                    id: upgrade.id,
                    name: upgrade.name,
                    price: upgrade.basePrice
                };
            });
            """
        )

        if not upgrades:
            return None

        return sorted(upgrades, key=lambda upgrade: upgrade["price"])[0]
