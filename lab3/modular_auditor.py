i = 0
f = 0

while True:
    s = input("Enter stock quantity or quit: ")

    if s == "quit":
        print("Total Units Processed:", i)
        print("Number of Failed/Rejected Entries:", f)
        break
    elif not s.isdigit():
        print("Error: Invalid input")
        f += 1
    else:
        n = int(s)

        if n < 0:
            print("Error: Negative numbers are not allowed")
            f += 1
        else:
            i += n

            if i > 500:
                print("Alert: Overstock")
                break