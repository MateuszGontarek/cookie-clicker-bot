class Product:
    def __init__(
        self,
        id: int,
        name: str,
        price: int,
        cps: float,
        web_element,
        is_avaiable: bool = False,
    ) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.cps = cps
        self.web_element = web_element
        self.is_avaiable = is_avaiable

    def calculate_ratio_per_price(self):
        return self.cps / self.price

    def __str__(self) -> str:
        return f"{self.name} - {self.price} - {self.calculate_ratio_per_price()} - {"avaiable" if self.is_avaiable else "locked"}"
