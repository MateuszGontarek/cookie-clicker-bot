from product import Product


class Products:
    def __init__(self) -> None:
        self.products_list: list[Product] = []

    def key_function(self, product: Product):
        return product.calculate_ratio_per_price()

    def best_to_buy(self) -> Product:
        filtered_products = list(
            filter(lambda product: product.is_avaiable == True, self.products_list)
        )

        if not filtered_products:
            return None

        sorted(filtered_products, key=self.key_function)
        print("next to buy:", filtered_products[-1])

        return filtered_products[-1]

    def add_product(self, product: Product) -> None:
        self.products_list.append(product)
