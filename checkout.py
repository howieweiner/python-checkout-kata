#!/usr/bin/python
class Checkout:
  running_total = 0
  rules = None
  item_count = {}

  def __init__(self, rules):
    self.rules = rules

    # seed item_count for provided items
    for k,v in rules.items(): 
      self.item_count[k] = 0

  def scan(self, item):
    """
    Extract price from rules for supplied item and add to running total
    Increment item count so discounts can be applied
    Apply any discounts
    """
    price = self._extract_price(item)
    if price:
      self.running_total += price
      self.item_count[item] += 1
      self._apply_discount(item)

  def total(self):
    return self.running_total

  def _extract_price(self, item):
    item = self.rules.get(item)
    if item:
      return item.get('price')
    return None

  def _apply_discount(self, item):
    """
    Check item count for supplied item. Then check discount threshold for the item
    in the rules. If a discount needs applying, adjust the total, and reset the item
    count.
    """
    count = self.item_count.get(item)
    item = self.rules.get(item)
    discount_threshold = item.get('discount_threshold')

    if discount_threshold and (count == discount_threshold):
      # calculate discount
      item_price = item.get('price')
      discount_price = item.get('discount_price')
      discount = (discount_threshold * item_price) - discount_price
      self.running_total -= discount

      # reset item count
      count = 0

    return
