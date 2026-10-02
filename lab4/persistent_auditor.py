def get_valid_input():
    s = input("Enter stock quantity or quit: ")

    if s == "quit":
        return "quit"
    elif not s.isdigit():
        print("Error: Invalid input")
        return None
    else:
        n = int(s)

        if n < 0:
            print("Error: Negative numbers are not allowed")
            return None
        else:
            return n


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return round(amount * 0.1, 2)


def generate_report(total_units, failed_attempts):
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

        total_units = 0
        transaction_history = []

        for line in lines:
            line = line.strip()

            if line.startswith("Total Units:"):
                total_units = int(line.split(":")[1].strip())

            elif line == "Transaction History:":
                continue

            elif line != "":
                transaction_history.append(int(line))

        return total_units, transaction_history

    except FileNotFoundError:
        print("No inventory file found. Starting with empty inventory.")
        return 0, []


def save_inventory(total_units, transaction_history):
    with open("inventory.txt", "w") as file:
        file.write("Total Units: " + str(total_units) + "\n")
        file.write("Transaction History:\n")

        for transaction in transaction_history:
            file.write(str(transaction) + "\n")


# Load previously saved inventory
i, transaction_history = load_inventory()

f = 0
total_tax = 0

while True:
    n = get_valid_input()

    if n == "quit":
        generate_report(i, f)
        print("Total Tax:", round(total_tax, 2))

        save_inventory(i, transaction_history)
        print("Inventory successfully saved to inventory.txt")

        break

    elif n is None:
        f += 1

    else:
        i = process_delivery(i, n)

        # Add valid transaction to history
        transaction_history.append(n)

        tax = calculate_tax(n)
        total_tax += tax
        print("Tax:", tax)

        if i > 500:
            print("Alert: Overstock")
            generate_report(i, f)
            print("Total Tax:", round(total_tax, 2))
            break