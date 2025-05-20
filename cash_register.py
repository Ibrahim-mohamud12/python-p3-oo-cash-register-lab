class CashRegister:
    def __init__(self, discount=0):
        self.discount = discount
        self.total = 0
        self.items = []
        self.transactions = []
        self.discount_applied = False  # Prevent multiple discounts

    def add_item(self, title, price, quantity=1):
        transaction_amount = price * quantity
        self.total += transaction_amount
        self.transactions.append((title, price, quantity))
        for _ in range(quantity):
            self.items.append(title)
        self.discount_applied = False  # <-- Reset discount flag when adding items

    def apply_discount(self):
        if self.discount > 0 and not self.discount_applied:
            discount_amount = self.total * (self.discount / 100)
            self.total -= discount_amount
            self.total = round(self.total)
            print(f"After the discount, the total comes to ${int(self.total)}.")
            self.discount_applied = True
        elif self.discount > 0 and self.discount_applied:
            print(f"After the discount, the total comes to ${int(self.total)}.")
        else:
            print("There is no discount to apply.")

    def void_last_transaction(self):
        if self.transactions:
            title, price, quantity = self.transactions.pop()
            self.total -= price * quantity
            for _ in range(quantity):
                if title in self.items:
                    self.items.remove(title)


import pytest
from cash_register import CashRegister

def test_initial_total_and_discount():
    register = CashRegister()
    assert register.total == 0
    assert register.discount == 0

def test_add_single_item():
    register = CashRegister()
    register.add_item("apple", 1.50)
    assert register.total == 1.50
    assert register.items == ["apple"]

def test_add_multiple_items():
    register = CashRegister()
    register.add_item("banana", 0.50, 3)
    assert register.total == 1.50
    assert register.items == ["banana", "banana", "banana"]

def test_apply_discount():
    register = CashRegister(discount=20)
    register.add_item("shirt", 25.00)
    register.apply_discount()
    assert register.total == 20

def test_apply_discount_no_discount():
    register = CashRegister()
    register.add_item("pants", 40.00)
    register.apply_discount()
    assert register.total == 40

def test_void_last_transaction():
    register = CashRegister()
    register.add_item("book", 10.00, 2)
    register.add_item("pen", 2.00)
    register.void_last_transaction()
    assert register.total == 20.00
    assert register.items == ["book", "book"]

def test_void_last_transaction_empty():
    register = CashRegister()
    register.void_last_transaction()  # Should not raise
    assert register.total == 0
    assert register.items == []