class Product:
    def __init__(
        self,
        id: int,
        name: str,
        price: int,
        cps: float,
        web_element,
        unlocked: bool = False,
    ) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.cps = cps
        self.web_element = web_element
        self.unlocked = unlocked

    def calculate_ratio_per_price(self):
        return self.cps / self.price

    def __str__(self) -> str:
        return f"{self.name} - {self.price} - {self.calculate_ratio_per_price()}"

    def buy(self):
        self.web_element.click()
