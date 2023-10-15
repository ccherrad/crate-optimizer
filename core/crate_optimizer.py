import math
from typing import List

from constants import CrateSlots
from persistance.load_data import DataProvider
from schemas.order import ProductOrder


class CrateOptimizer:
    def __init__(self, order_products: List[ProductOrder], data_provider: DataProvider):
        """
        Initialize the CrateOptimizer.

        Parameters:
        - order_products (List[ProductOrder]): A list of product orders to be optimized.
        - data_provider (DataProvider): An instance of the DataProvider class.

        Raises:
        - ValueError: If order_products have different orderId values.
        """
        self.order_products = order_products
        self.data_provider = data_provider

        if not all(
            order_product.orderId == order_products[0].orderId
            for order_product in order_products
        ):
            raise ValueError("order_products have different orderId values.")

        self.crate_counts = {"Supplier": 0, "Slot6": 0, "Slot12": 0, "Slot20": 0}

    # This is non pure function because it is changing the status outside it.
    def is_kept_in_crate(self, order_product):
        """
        Determine if an order product is kept in a crate and update crate counts.

        Parameters:
        - order_product (ProductOrder): An order product to be checked.

        Returns:
        - ProductOrder: The order product with updated unit count.

        """
        product_info = self.data_provider.get_product_by_sku(order_product.sku)
        if (
            product_info["preparation_in_crate"] == True
            and product_info["brand"] != "La Tournée"
            and order_product.unitCount >= product_info["packing"]
        ):
            print(order_product)
            self.crate_counts["Supplier"] += (
                order_product.unitCount // product_info["packing"]
            )
            remaining_units = order_product.unitCount % product_info["packing"]
        else:
            remaining_units = order_product.unitCount

        order_product.unitCount = remaining_units
        return order_product

    # this is the same but it is just checking.
    def is_kept_in_supplier_crate(self, order_product):
        product_info = self.data_provider.get_product_by_sku(order_product.sku)
        return (
            product_info["preparation_in_crate"] == True
            and product_info["brand"] != "La Tournée"
        )

    def is_orangina(self, order_product):
        """
        Check if an order product is an "orangina" product.

        Parameters:
        - order_product (ProductOrder): An order product to be checked.

        Returns:
        - bool: True if the product is an "orangina" product, False otherwise.
        """
        product_info = self.data_provider.get_product_by_sku(order_product.sku)

        return "orangina" in product_info["sku"]

    def is_latournee_order_product(self, order_product):
        """
        Check if an order product is from the "La Tournée" brand.

        Parameters:
        - order_product (ProductOrder): An order product to be checked.

        Returns:
        - bool: True if the product is from the "La Tournée" brand, False otherwise.
        """
        product_info = self.data_provider.get_product_by_sku(order_product.sku)

        return product_info["brand"] == "La Tournée"

    def is_small_order_product(self, order_product):
        """
        Check if an order product is a small product.

        Parameters:
        - order_product (ProductOrder): An order product to be checked.

        Returns:
        - bool: True if the product is a small product, False otherwise.
        """
        product_info = self.data_provider.get_product_by_sku(order_product.sku)
        is_orangina = self.is_orangina(order_product)
        is_latournee = self.is_latournee_order_product(order_product)
        is_small = product_info["deposit"] != 0.2

        return not any([is_orangina, is_latournee, is_small])

    def is_other_order_product(self, order_product):
        """
        Check if an order product is categorized as "other."

        Parameters:
        - order_product (ProductOrder): An order product to be checked.

        Returns:
        - bool: True if the product is categorized as "other," False otherwise.
        """
        conditions = [
            self.is_kept_in_supplier_crate(order_product),
            not self.is_orangina(order_product),
            self.is_small_order_product(order_product),
            self.is_latournee_order_product(order_product),
        ]

        return not any(conditions)

    def calculate_optimal_crates(self):
        """
        Calculate the optimal distribution of products into crates.

        Returns:
        - dict: A dictionary containing counts of crates for each type.
        """
        needed_slots = 0
        self.order_products = list(
            map(lambda product: self.is_kept_in_crate(product), self.order_products)
        )

        small_needed_slots = 0
        small_product_orders = list(
            filter(
                lambda product: self.is_small_order_product(product),
                self.order_products,
            )
        )

        small_needed_slots += sum(
            order_product.unitCount for order_product in small_product_orders
        )
        self.crate_counts["Slot20"] = (
            small_needed_slots + 1
        ) // CrateSlots.Slot20.value
        if (small_needed_slots) % CrateSlots.Slot20.value:
            self.crate_counts["Slot20"] += 1

        orangina_product_orders = list(
            filter(lambda product: self.is_orangina(product), self.order_products)
        )
        needed_slots += (
            sum(order_product.unitCount for order_product in orangina_product_orders)
            + 1
        ) // 2

        latournee_product_orders = list(
            filter(
                lambda product: self.is_latournee_order_product(product),
                self.order_products,
            )
        )

        # TODO: 1.2 should be moved to constants.
        # 6/5 is 1.2 that we use to deal with La Tournee products.
        needed_slots += math.ceil(
            (sum(order_product.unitCount for order_product in latournee_product_orders))
            * 1.2
        )

        other_product_orders = list(
            filter(
                lambda product: self.is_other_order_product(product),
                self.order_products,
            )
        )
        needed_slots += sum(
            order_product.unitCount for order_product in other_product_orders
        )

        self.crate_counts["Slot12"] = needed_slots // CrateSlots.Slot12.value
        remaining_needed = needed_slots % CrateSlots.Slot12.value
        if remaining_needed > CrateSlots.Slot6.value:
            self.crate_counts["Slot12"] += 1
        else:
            self.crate_counts["Slot6"] = needed_slots // CrateSlots.Slot6.value
            if needed_slots % CrateSlots.Slot6.value:
                self.crate_counts["Slot6"] += 1

        return self.crate_counts
