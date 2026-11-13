
import json
import os
from abc import ABC, abstractmethod

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_email = contact_email

    def display_information(self) -> None:
        print("Supplier ID:", self.supplier_id)
        print("Supplier Name:", self.name)
        print("Supplier Email:", self.contact_email)


default_supplier = Supplier("S001", "Default Supplier", "supplier@example.com")

class Product(ABC):
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier: Supplier = supplier

    def update_stock(self, quantity: int) -> None:
        self.__stock = quantity

    def get_product_id(self) -> str:
        return self.__product_id

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def get_price(self) -> float:
        return self.__price

    def display_information(self) -> None:
        print("------------------------------------------------")
        print("ID:", self.__product_id)
        print("Name:", self.__name)
        print("Price: $%.2f" % self.__price)
        print("Stock:", self.__stock)
        print("------------------------------------------------")

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight = weight

    def display_information(self) -> None:
        super().display_information()
        print("Weight:", self.__weight, "kg")

    def get_fulfilment_info(self) -> str:
        return "This product will be shipped to the customer."

    def calculate_shipping_cost(self) -> float:
        return self.__weight * 2

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print("Download Size:", self.__download_size, "MB")

    def get_fulfilment_info(self) -> str:
        return "This product will be delivered digitally."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data


class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id: str) -> None:
        for p in self.__products:
            if p.get_product_id() == product_id:
                self.__products.remove(p)
                return

    def find_product(self, product_id: str) -> Product | None:
        for p in self.__products:
            if p.get_product_id() == product_id:
                return p
        return None

    def display_all(self) -> None:
        print("Current Inventory")
        print("------------------------------------------------")

        for p in self.__products:
            p.display_information()

        print("------------------------------------------------")

    def get_all_products(self) -> list[Product]:
        return self.__products

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(self.__product.get_product_id(), "x", self.__quantity,
              "= $%.2f" % self.calculate_subtotal())


class Order:
    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, index: int) -> None:
        self.__order_lines.pop(index)

    def calculate_total(self) -> float:
        total = 0.0
        for line in self.__order_lines:
            total += line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print("Order:", self.__order_id)
        for line in self.__order_lines:
            line.display_information()
        print("Total: $%.2f" % self.calculate_total())

def load_inventory() -> Inventory:
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
                    default_supplier,
                    p.get("weight", 1.0)
                )

            elif product_type == "digital":
                product = DigitalProduct(
                    p["id"],
                    p["name"],
                    p["price"],
                    p["stock"],
                    default_supplier,
                    p.get("download_size", 0.0)
                )

            else:
                continue

            inventory.add_product(product)

        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")

    if inventory.find_product("P001") is None:
        product1 = PhysicalProduct("P001", "Laptop", 1200.00, 15, default_supplier, 2.5)
        inventory.add_product(product1)

    if inventory.find_product("P002") is None:
        product2 = PhysicalProduct("P002", "Mouse", 25.50, 40, default_supplier, 0.2)
        inventory.add_product(product2)

    return inventory


def save_inventory(inventory: Inventory) -> None:
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


def add_product(inventory: Inventory) -> None:
    print("Add New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    choice = input("Choose product type: ")

    if choice not in ("1", "2"):
        print("Invalid product type.")
        return

    pid = input("Product ID: ")

    if inventory.find_product(pid) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    if choice == "1":
        weight = float(input("Weight (kg): "))
        product = PhysicalProduct(pid, name, price, stock, default_supplier, weight)

    else:
        download_size = float(input("Download Size (MB): "))
        product = DigitalProduct(pid, name, price, stock, default_supplier, download_size)

    inventory.add_product(product)

    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("Update Stock")

    pid = input("Enter Product ID: ")

    product = inventory.find_product(pid)

    if product is not None:
        print("Product Found:")
        product.display_information()

        new_stock = int(input("New Stock Quantity: "))

        product.update_stock(new_stock)

        print("Stock updated successfully!")

    else:
        print("Product not found.")


def find_product(inventory: Inventory) -> None:
    print("Find Product")

    pid = input("Enter Product ID: ")

    product = inventory.find_product(pid)

    if product is not None:
        print("Product Found")
        product.display_information()
        print(product.get_fulfilment_info())

        if isinstance(product, CanBeShipped):
            print("Shipping Cost: $%.2f" % product.calculate_shipping_cost())

    else:
        print("Product not found.")


def display_all(inventory: Inventory) -> None:
    inventory.display_all()

def test_association() -> None:
    supplier = Supplier("S100", "TechSource Ltd", "sales@techsource.com")
    laptop = PhysicalProduct("T001", "Test Laptop", 1000.0, 5, supplier, 2.0)
    ebook = DigitalProduct("T002", "Test Ebook", 15.0, 100, supplier, 5.0)

    laptop.get_supplier().display_information()
    ebook.get_supplier().display_information()

    del supplier
    print("After del supplier:")
    laptop.get_supplier().display_information()


test_association()

def test_aggregation() -> None:
    supplier = Supplier("S100", "TechSource Ltd", "sales@techsource.com")
    laptop = PhysicalProduct("T001", "Test Laptop", 1000.0, 5, supplier, 2.0)

    inventory_a = Inventory()
    inventory_b = Inventory()

    inventory_a.add_product(laptop)
    print("Inventory A has laptop:", inventory_a.find_product("T001") is laptop)

    inventory_a.remove_product("T001")
    print("Inventory A has laptop:", inventory_a.find_product("T001") is laptop)

    print("Laptop still usable after removal:")
    laptop.display_information()

    inventory_b.add_product(laptop)
    print("Inventory B has laptop:", inventory_b.find_product("T001") is laptop)

test_aggregation()

def test_composition() -> None:
    supplier = Supplier("S100", "TechSource Ltd", "sales@techsource.com")
    laptop = PhysicalProduct("T001", "Test Laptop", 1000.0, 5, supplier, 2.0)
    ebook = DigitalProduct("T002", "Test Ebook", 15.0, 100, supplier, 5.0)

    order1 = Order("O001")
    order1.add_order_line(laptop, 2)
    order1.add_order_line(ebook, 3)
    order1.display_information()

    order2 = Order("O002")
    order2.add_order_line(laptop, 1)
    order2.display_information()

    order1.remove_order_line(0)
    print("After removing line 0 from order 1:")
    order1.display_information()

    print("Laptop still usable:")
    laptop.display_information()

test_composition()

print("========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("========================================")

inventory = load_inventory()

while True:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Find Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("7. Run Tests")
    print("----------------------------")

    option = input("Enter option: ")

    if option == "1":
        display_all(inventory)

    elif option == "2":
        add_product(inventory)

    elif option == "3":
        update_stock(inventory)

    elif option == "4":
        find_product(inventory)

    elif option == "5":
        save_inventory(inventory)

    elif option == "7":
        test_composition()

    elif option == "6":
        print("Saving inventory before exit...")
        save_inventory(inventory)
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break

    else:
        print("Invalid option.")