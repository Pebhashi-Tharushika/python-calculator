cal_list = []

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    try:
        return a / b
    except Exception as e:
        print(e)


def power(a, b):
    return a ** b


def remainder(a, b):
    return a % b


def history():
    if len(cal_list) == 0:
        print("No past calculations to show")
    else:
        for cal in cal_list:
            print(cal)


def select_op(selection):
    if selection == '#':
        return -1
    elif selection == '$':
        return 0
    elif selection == '?':
        history()
        return 0
    elif selection in ('+', '-', '*', '/', '^', '%'):
        num1 = 0.0
        num2 = 0.0
        result = 0.0

        while True:
            num1s = str(input("Enter Calculator number: "))
            print(num1s)
            if num1s.endswith('$'):
                return 0
            if num1s.endswith('#'):
                return -1

            try:
                num1 = float(num1s)
                break
            except ValueError:
                print("Not a valid number,please enter again")
                continue

        while True:
            num2s = str(input("Enter second number: "))
            print(num2s)
            if num2s.endswith('$'):
                return 0
            if num2s.endswith('#'):
                return -1
            try:
                num2 = float(num2s)
                break
            except ValueError:
                print("Not a valid number,please enter again")
                continue


        if selection == '+':
            result = add(num1, num2)
        elif selection == '-':
            result = subtract(num1, num2)
        elif selection == '*':
            result = multiply(num1, num2)
        elif selection == '/':
            result = divide(num1, num2)
        elif selection == '^':
            result = power(num1, num2)
        elif selection == '%':
            result = remainder(num1, num2)
        else:
            print("Something Went Wrong")

        last_calculation = "{0} {1} {2} = {3}".format(num1, selection, num2, result)
        print(last_calculation)
        cal_list.append(last_calculation)

    else:
        print("Unrecognized operation")


while True:
    print("Select operation.")
    print("1.Add      : + ")
    print("2.Subtract : - ")
    print("3.Multiply : * ")
    print("4.Divide   : / ")
    print("5.Power    : ^ ")
    print("6.Remainder: % ")
    print("7.Terminate: # ")
    print("8.Reset    : $ ")
    print("8.History  : ? ")

    # take input from the user
    choice = input("Enter choice(+,-,*,/,^,%,#,$,?): ")
    print(choice)
    if select_op(choice) == -1:
        # program ends here
        print("Done. Terminating")
        exit()


