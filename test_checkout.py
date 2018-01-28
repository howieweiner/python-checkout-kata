#!/usr/bin/python
import unittest
import checkout

RULES = {
  'A': {'price': 50, 'discount_threshold': 3, 'discount_price': 130},
  'B': {'price': 30, 'discount_threshold': 2, 'discount_price': 45},
  'C': {'price': 20},
  'D': {'price': 15}
}

def calc_price(items):
  co = checkout.Checkout(RULES)
  for item in items:
    co.scan(item)
  return co.total()

class TestBasket(unittest.TestCase):
  def test_complex_basket(self):
    total = calc_price('DABABA')
    self.assertEqual(190, total)

class TestTotals(unittest.TestCase):
  def setUp(self):
    self.co = checkout.Checkout(RULES)

  def test_no_item(self):
    self.co.scan('')
    total = self.co.total()
    self.assertEqual(0, total)

  def test_invalid_item(self):
    self.co.scan('Z')
    total = self.co.total()
    self.assertEqual(0, total)

  def test_single_item(self):
    self.co.scan('A')
    total = self.co.total()
    self.assertEqual(50, total)

  def test_two_single_items(self):
    self.co.scan('A')
    self.co.scan('B')
    total = self.co.total()
    self.assertEqual(80, total)

  def test_discount(self):
    self.co.scan('B')
    self.co.scan('B')
    total = self.co.total()
    self.assertEqual(45, total)

  def test_normal_price_after_discount(self):
    self.co.scan('B')
    self.co.scan('B')
    self.co.scan('B')
    total = self.co.total()
    self.assertEqual(75, total)

if __name__ == "__main__":
  unittest.main()