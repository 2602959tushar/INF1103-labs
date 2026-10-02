import json


def load_inventory():
    try:
        file = open("inventory.json", "r")
        data = json.load(file)
        file.close()
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return data
    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")
        return []


def save_inventory(inventory):
    print("Saving inventory...")
    file = open("inventory.json", "w")
    json.dump(inventory, file)
    file.close()
    print("Inventory saved successfully to inventory.json.")


def add_product(inventory):
    print("Add New Product")
    pid = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))
    inventory.append({"id": pid, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")


def update_stock(inventory):
    print("Update Stock")
    pid = input("Enter Product ID: ")
    for p in inventory:
        if p["id"] == pid:
            print("Product Found:")
            print("Name:", p["name"])
            print("Current Stock:", p["stock"])
            new_stock = int(input("New Stock Quantity: "))
            p["stock"] = new_stock
            print("Stock updated successfully!")
            return
    print("Product not found.")


def search_product(inventory):
    print("Search Product")
    pid = input("Enter Product ID: ")
    for p in inventory:
        if p["id"] == pid:
            print("Product Found")
            print("------------------------------------------------")
            print("ID:", p["id"])
            print("Name:", p["name"])
            print("Price: $%.2f" % p["price"])
            print("Stock:", p["stock"])
            print("------------------------------------------------")
            return
    print("Product not found.")


def display_all(inventory):
    print("Current Inventory")
    print("------------------------------------------------")
    for p in inventory:
        print("ID: %s | Name: %s | Price: $%.2f | Stock: %d" % (p["id"], p["name"], p["price"], p["stock"]))
    print("------------------------------------------------")


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