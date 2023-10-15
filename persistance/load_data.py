"""Import Store data fron a json file
"""
import structlog
import os
import json

from exceptions.persistance import ProductNotFound

logger = structlog.get_logger(__name__)


MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


class DataProvider:
    DATA_FILE_PATH = os.path.join(MODULE_DIR, "store.json")

    def __init__(self):
        self.data = self.load_data()

    def load_data(self) -> list[dict]:
        """Load data from a json file"""
        with open(self.DATA_FILE_PATH, "r") as filed:
            return json.load(filed)

    def get_product_by_sku(self, sku):
        for product in self.data:
            if product.get("sku") == sku:
                return product
        raise ProductNotFound(sku)


data_provider = DataProvider()


def get_data_provider():
    return data_provider
