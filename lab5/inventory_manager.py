def add_product(inventory):
    pid = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))
    inventory.append({"id": pid, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")


def display_all(inventory):
    print("Current Inventory")
    print("------------------------------------------------")
    for p in inventory:
        print("ID: %s | Name: %s | Price: $%.2f | Stock: %d" % (p["id"], p["name"], p["price"], p["stock"]))
    print("------------------------------------------------")


inventory = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
]

display_all(inventory)
add_product(inventory)
display_all(inventory)