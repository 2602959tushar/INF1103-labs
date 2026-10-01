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


def save_inventory(total_units, transaction_history):
    with open("inventory.txt", "w") as file:
        file.write("Total Units: " + str(total_units) + "\n")
        file.write("Transaction History:\n")

        for transaction in transaction_history:
            file.write(str(transaction) + "\n")


i = 0
f = 0
total_tax = 0

# History tracking
transaction_history = []

while True:
    n = get_valid_input()

    if n == "quit":
        generate_report(i, f)
        print("Total Tax:", round(total_tax, 2))

        # Write final total and transaction history to file
        save_inventory(i, transaction_history)
        print("Inventory successfully saved to inventory.txt")

        break

    elif n is None:
        f += 1

    else:
        i = process_delivery(i, n)

        # Add every valid transaction to the history list
        transaction_history.append(n)

        tax = calculate_tax(n)
        total_tax += tax
        print("Tax:", tax)

        if i > 500:
            print("Alert: Overstock")
            generate_report(i, f)
            print("Total Tax:", round(total_tax, 2))
            break