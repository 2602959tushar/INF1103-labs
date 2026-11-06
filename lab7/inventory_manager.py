
import json
import os
from abc import ABC, abstractmethod


class Product(ABC):
    @abstractmethod
    def get_fulfilment_info(self):
        pass

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, quantity):
        self.__stock = quantity

    def get_product_id(self):
        return self.__product_id

    def display_information(self):
        print("------------------------------------------------")
        print("ID:", self.__product_id)
        print("Name:", self.__name)
        print("Price: $%.2f" % self.__price)
        print("Stock:", self.__stock)
        print("------------------------------------------------")

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def display_information(self):
        super().display_information()
        print("Weight:", self.__weight, "kg")

    def get_fulfilment_info(self):
        return "This product will be shipped to the customer."

    def calculate_shipping_cost(self):
        return self.__weight * 2

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def display_information(self):
        super().display_information()
        print("Download Size:", self.__download_size, "MB")

    def get_fulfilment_info(self):
        return "This product will be delivered digitally."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for p in self.__products:
            if p.get_product_id() == product_id:
                return p
        return None

    def display_all(self):
        print("Current Inventory")
        print("------------------------------------------------")

        for p in self.__products:
            p.display_information()

        print("------------------------------------------------")

    def get_all_products(self):
        return self.__products


def load_inventory():
    inventory = Inventory()

    inventory_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "inventory.json"
    )

    try:
        with open(inventory_file, "r") as file:
            content = file.read()

            if content.strip() == "":
                data = []
            else:
                data = json.loads(content)

        print("inventory.json found.")

        for p in data:
            product_type = p.get("type", "physical")

            if product_type == "physical":
                product = PhysicalProduct(
                    p["id"],
                    p["name"],
                    p["price"],
                    p["stock"],
                    p.get("weight", 1.0)
                )

            elif product_type == "digital":
                product = DigitalProduct(
                    p["id"],
                    p["name"],
                    p["price"],
                    p["stock"],
                    p.get("download_size", 0.0)
                )

            else:
                continue

            inventory.add_product(product)

        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")

    if inventory.search_product("P001") is None:
        product1 = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5)
        inventory.add_product(product1)

    if inventory.search_product("P002") is None:
        product2 = PhysicalProduct("P002", "Mouse", 25.50, 40, 0.2)
        inventory.add_product(product2)

    return inventory


def save_inventory(inventory):
    print("Saving inventory...")

    data = []

    for p in inventory.get_all_products():
        data.append(p.to_dict())

    inventory_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "inventory.json"
    )

    with open(inventory_file, "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


def add_product(inventory):
    print("Add New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    choice = input("Choose product type: ")

    if choice not in ("1", "2"):
        print("Invalid product type.")
        return

    pid = input("Product ID: ")

    if inventory.search_product(pid) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    if choice == "1":
        weight = float(input("Weight (kg): "))
        product = PhysicalProduct(pid, name, price, stock, weight)

    else:
        download_size = float(input("Download Size (MB): "))
        product = DigitalProduct(pid, name, price, stock, download_size)

    inventory.add_product(product)

    print("Product added successfully!")


def update_stock(inventory):
    print("Update Stock")

    pid = input("Enter Product ID: ")

    product = inventory.search_product(pid)

    if product is not None:
        print("Product Found:")
        product.display_information()

        new_stock = int(input("New Stock Quantity: "))

        product.update_stock(new_stock)

        print("Stock updated successfully!")

    else:
        print("Product not found.")


def search_product(inventory):
    print("Search Product")

    pid = input("Enter Product ID: ")

    product = inventory.search_product(pid)

    if product is not None:
        print("Product Found")
        product.display_information()
        print(product.get_fulfilment_info())

        if isinstance(product, CanBeShipped):
            print("Shipping Cost: $%.2f" % product.calculate_shipping_cost())

    else:
        print("Product not found.")


def display_all(inventory):
    inventory.display_all()


print("========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("========================================")

inventory = load_inventory()

while True:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

    option = input("Enter option: ")

    if option == "1":
        display_all(inventory)

    elif option == "2":
        add_product(inventory)

    elif option == "3":
        update_stock(inventory)

    elif option == "4":
        search_product(inventory)

    elif option == "5":
        save_inventory(inventory)

    elif option == "6":
        print("Saving inventory before exit...")
        save_inventory(inventory)
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break

    else:
        print("Invalid option.")