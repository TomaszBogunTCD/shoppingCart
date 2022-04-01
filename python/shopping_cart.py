from abc import ABC, abstractmethod
from typing import Dict

from shopping_cart_interface import IShoppingCart
from pricer import Pricer

class ShoppingCart(IShoppingCart):
    """
    Implementation of the shopping tills in our supermarket.
    """
    def __init__(self, pricer: Pricer):
        self.pricer = pricer
        self._contents: Dict[str,int] = {}
        self.itemScanOrder = []
        # retrieves the format for receipt printing from a local file
        try:
            f = open("receiptPrintFormat.txt", "r")
            self.receiptPrintFormat = f.read()
            f.close()
        # if the format file is not found, the format for printing is set to the default printing format
        except FileNotFoundError:
            self.receiptPrintFormat = "ITEM: PRICE x QUANTITY = TOTAL"

    def add_item(self, itemName: str, quantity: int):
        # checks the itemName to see if there are any reserved capitalised keywords
        # that are used exclusively for formatting the receipt print functionality.
        # replaces them with the lowercase version if they are in the name
        if "TOTAL" in itemName or "ITEM" in itemName or "QUANTITY" in itemName or "PRICE" in itemName:
            itemName.replace("TOTAL", "total").replace("ITEM", "item").replace("QUANTITY", "quantity").replace("PRICE", "price")
        # adds new item to or update existing item in the shopping cart
        # appends the item onto the scan order array if first time scanning such item
        if itemName not in self._contents:
            self.itemScanOrder.append(itemName)
            self._contents[itemName] = quantity
        else:
            self._contents[itemName] = self._contents[itemName] + quantity


    # prints prices in euros instead of euro cents (eg. €1.56) by dividing the price in eurocents by 100, always with 2 digits after the decimal point
    def print_receipt(self):
        total = 0
        # prints items in the order the were scanned
        for itemName in self.itemScanOrder:
            quantity = self._contents[itemName]
            price = self.pricer.get_price(itemName)
            price /= 100
            total += (price * quantity)
            self.print_receipt_line(itemName, price, quantity)
        print("total: " + "{:.2f}".format(total))

    def print_receipt_line(self, itemName, price, quantity):
        # a line in the receipt is printed by replacing all capitalised reserved keywords by the passed in variables
        print(self.receiptPrintFormat
              .replace("ITEM", str(itemName))
              .replace("PRICE", str("{:.2f}".format(price)))
              .replace("QUANTITY", str(quantity))
              .replace("TOTAL", str("{:.2f}".format(price * quantity))))


class ShoppingCartCreator(ABC):
    """
    Interface for the ShoppingCart creator.
    The creation process will be delegated to the subclasses of this class.
    """
    @abstractmethod
    def factory_method(self) -> ShoppingCart:
        # return the ShoppingCart object
        pass

    def operation(self) -> ShoppingCart:
        # Here more operations can be performed on the ShoppingCart object
        # returns ShoppingCart object
        return self.factory_method()

class ShoppingCartConcreteCreator(ShoppingCartCreator):
    """
    Concrete class for the ShoppingCart creator.
    Implements the factory_method
    """
    def factory_method(self) -> ShoppingCart:
        # returns ShoppingCart object
        return ShoppingCart(Pricer())
