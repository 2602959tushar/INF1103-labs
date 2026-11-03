import json
import os

class Product:
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
            product = Product(
                p["id"],
                p["name"],
                p["price"],
                p["stock"]
            )

            inventory.add_product(product)

        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")

    product1 = Product("P001", "Laptop", 1200.00, 15)
    product2 = Product("P002", "Mouse", 25.50, 40)

    if inventory.search_product("P001") is None:
        inventory.add_product(product1)

    if inventory.search_product("P002") is None:
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

    pid = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    product = Product(pid, name, price, stock)

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