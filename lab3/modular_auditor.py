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
i = 0
f = 0

while True:
    n = get_valid_input()

    if n == "quit":
        print("Total Units Processed:", i)
        print("Number of Failed/Rejected Entries:", f)
        break
    elif n is None:
        f += 1
    else:
        i += n

    if i > 500:
        print("Alert: Overstock")
        print("Total Units Processed:", i)
        print("Number of Failed/Rejected Entries:", f)
        break