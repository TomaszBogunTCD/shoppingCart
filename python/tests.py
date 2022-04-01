import unittest

from shopping_cart import ShoppingCartConcreteCreator
from test_utils import Capturing

class ShoppingCartTest(unittest.TestCase):
    def test_print_receipt(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc.add_item("apple", 2)
        with Capturing() as output:
            sc.print_receipt()

        self.assertEqual(sc.receiptPrintFormat.replace("ITEM", "apple").replace("PRICE", "1.00").replace("QUANTITY", "2").replace("TOTAL", "2.00"), output[0])
        self.assertEqual("total: 2.00", output[1])

    def test_non_existent_item(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc.add_item("apple", 2)
        sc.add_item("banana", 5)
        sc.add_item("pear", 5)
        with Capturing() as output:
            sc.print_receipt()

        self.assertEqual(sc.receiptPrintFormat.replace("ITEM", "apple").replace("PRICE", "1.00").replace("QUANTITY", "2").replace("TOTAL", "2.00"), output[0])
        self.assertEqual(sc.receiptPrintFormat.replace("ITEM", "banana").replace("PRICE", "2.00").replace("QUANTITY", "5").replace("TOTAL", "10.00"), output[1])
        self.assertEqual(sc.receiptPrintFormat.replace("ITEM", "pear").replace("PRICE", "0.00").replace("QUANTITY", "5").replace("TOTAL", "0.00"), output[2])
        self.assertEqual("total: 12.00", output[3])

    def test_no_items(self):
        sc = ShoppingCartConcreteCreator().operation()
        with Capturing() as output:
            sc.print_receipt()
        self.assertEqual("total: 0.00", output[0])

    def test_same_item_multiple_scans(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc.add_item("apple", 1)
        sc.add_item("apple", 2)
        sc.add_item("apple", 3)
        with Capturing() as output:
            sc.print_receipt()

        self.assertEqual(sc.receiptPrintFormat.replace("ITEM", "apple").replace("PRICE", "1.00").replace("QUANTITY", "6").replace("TOTAL", "6.00"), output[0])
        self.assertEqual("total: 6.00", output[1])

    # test if the order of the items printed is the same as the order they were scanned, even if they
    def test_items_location_shuffled(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc.add_item("apple", 1)
        sc.add_item("banana", 3)
        sc.add_item("apple", 4)
        with Capturing() as output:
            sc.print_receipt()

        self.assertEqual(sc.receiptPrintFormat.replace("ITEM", "apple").replace("PRICE", "1.00").replace("QUANTITY", "5").replace("TOTAL", "5.00"), output[0])
        self.assertEqual(sc.receiptPrintFormat.replace("ITEM", "banana").replace("PRICE", "2.00").replace("QUANTITY", "3").replace("TOTAL", "6.00"), output[1])
        self.assertEqual("total: 11.00", output[2])

    # test support for fractional quantities
    # eg 0.5 watermelon
    def test_fractional_quantity(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc.add_item("apple", 1.5)
        with Capturing() as output:
            sc.print_receipt()
        self.assertEqual(sc.receiptPrintFormat.replace("ITEM", "apple").replace("PRICE", "1.00").replace("QUANTITY", "1.5").replace("TOTAL", "1.50"), output[0])


unittest.main(exit=False)
