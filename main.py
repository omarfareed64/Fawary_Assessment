
from datetime import datetime
class Product:
    def __init__(self, name, price, expires=None,expiry_date=None,weight=0,quantity=None,shipping_price=None):
        self.name = name
        self.price = price
        self.expires = expires
        self.weight = weight
        self.quantity = quantity 
        self.expiry_date = expiry_date
        self.shipping_price =  shipping_price
    # check if the product needs shipping based on its weight and type
    def need_shipping(self):
        if self.weight is not None and self.weight > 1 and self.name.lower() in ["cheese", "tv"]:
            return True
        return False
    # check if the product is expired or not
    def is_expired(self):
        if self.expires and self.expiry_date:
            return datetime.now() > self.expiry_date
        return False
    # function to be able print the product details
    def __str__(self):
        return f"{self.name}: ${self.price:.2f}"

class ShoppingCart:
    def __init__(self):
        self.items = {}
    # function to be able to iterate over the items in the cart
    def __iter__(self):
        return iter(self.items.items())
    # function to add a product to the cart
    def add_product(self, product, quantity):
        if product.is_expired():
            raise ValueError(f"{product.name} is expired.")
        if quantity > product.quantity:
            raise ValueError("Not enough in stock.")
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity
        product.quantity -= quantity
    # function to remove a product from the cart
    def remove_product(self, product):
        if product in self.items:
            del self.items[product]
        else:
            raise ValueError(f"{product.name} not found in cart.")

class ShippingService:
    @staticmethod
    # Function to ship items in the cart
    def ship(items):
        print("** Shipment notice **")
        total_weight = 0
        for product, quantity in items.items():
            if product.need_shipping():
                print(f"{quantity}x {product.name} {product.weight}g")
                total_weight += (product.weight * quantity)
        print(f"Total package weight: {total_weight / 1000}kg")

class Customer:
    def __init__(self, name, balance=0,cart=None):
        self.name = name
        self.balance = balance 
        self.cart = ShoppingCart()
    # function to add a product to the cart
    def add_to_cart(self, product):
        self.cart.add_product(product,quantity=1)
    # function to remove a product from the cart
    def remove_from_cart(self, product):
        self.cart.remove_product(product)
    # function to checkout the cart
    def checkout(self):
        if not self.cart.items:
            print("Your cart is empty.")
            return

        # Shipping Notice
        print("** Shipment notice **")
        total_weight = 0
        shipping_cost = 0
        for product, quantity in self.cart:
            if product.need_shipping():
                print(f"{quantity}x {product.name} {product.weight}g")
                total_weight += product.weight * quantity
                shipping_cost += (product.weight * quantity) *  0.0366666666666667 #my assumption of shipping cost per gram taken from calculation of the usecase provided 

        print(f"Total package weight {total_weight / 1000}kg")

    
        print("** Checkout receipt **")
        subtotal = 0
        # Print each product in the cart with its quantity and total price
        for product, quantity in self.cart:
            line_total = product.price * quantity
            print(f"{quantity}x {product.name} {line_total}")
            subtotal += line_total
        print("----------------------")
        print(f"Subtotal {subtotal}")
        print(f"Shipping {int(shipping_cost)}")
        print(f"Amount {int(subtotal + shipping_cost)}")

        if subtotal + shipping_cost > self.balance:
            print("Insufficient balance.")
            return

        self.balance -= (subtotal + shipping_cost)
        self.cart.items.clear()
if __name__ == "__main__":
    # Example usage
    #provide the quantity of the product in the constructor
    scratch_card = Product("Scratch Card", 50, quantity=10)
    cheese = Product("Cheese", 100, expires=True, expiry_date=datetime(2023, 10, 1), weight=200, quantity=5)
    tv = Product("TV", 1000, weight=5000, quantity=2)

    customer = Customer("Omar", balance=5000)
    customer.cart.add_product(cheese, 2)
    customer.cart.add_product(tv, 1)
    customer.cart.add_product(scratch_card, 1)
    customer.checkout()
