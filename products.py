from product import Product


class Products:
    def __init__(self, driver) -> None:
        self.driver = driver

        self.products_list: list[Product] = []
        self.next_avaiable_product_index: int = 1

        for product_item in self.driver.get_buildings():
            product = Product(
                id=product_item["id"],
                name=product_item["name"],
                price=product_item["price"],
                cps=product_item["cps"],
                web_element=self.driver.find_product(product_item["id"]),
                unlocked=not product_item["locked"],
            )

            self.add_product(product)

        self.product_to_buy = self.best_to_buy()

    def key_function(self, product: Product):
        return product.calculate_ratio_per_price()

    def best_to_buy(self) -> Product:
        filtered_products = list(
            filter(lambda product: product.unlocked == True, self.products_list)
        )

        if not filtered_products:
            return None

        sorted(filtered_products, key=self.key_function)
        print("next to buy:", filtered_products[-1])

        return filtered_products[-1]

    def add_product(self, product: Product) -> None:
        self.products_list.append(product)

    def __str__(self) -> str:
        return "\n".join([str(product) for product in self.products_list])

    def check_if_next_product_unlocked(self) -> None:
        if self.driver.get_product_unlocked(self.next_avaiable_product_index):
            product = self.products_list[self.next_avaiable_product_index]

            product.unlocked = True

            self.next_avaiable_product_index += 1

    def buy_product(self, cookie_count: int) -> int:
        if cookie_count < self.product_to_buy.price:
            return 0

        price = self.product_to_buy.price

        self.product_to_buy.buy()
        self.product_to_buy.price = self.driver.get_new_price_for_building(
            self.product_to_buy.id
        )

        self.product_to_buy = self.best_to_buy()
        return price
