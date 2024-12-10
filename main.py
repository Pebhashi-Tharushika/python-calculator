import os
import math

# History lists for each menu
basic_cal_list = []
advanced_cal_list = []
trigonometric_cal_list = []
programming_cal_list = []

# Define menus dictionary
menus = {
    "main": ("WELCOME!", [
        ("Basic", "BAS"),
        ("Advanced", "ADV"),
        ("Trigonometric", "TRI"),
        ("Programming", "PRO"),
        ("Terminate", "#")
    ]),
    "basic": ("BASIC", [
        ("Addition", "+"),
        ("Subtraction", "-"),
        ("Multiplication", "*"),
        ("Division", "/"),
        ("Square", "^"),
        ("Square Root", "√"),
        ("Remainder", "mod"),
        ("History", "?"),
        ("Back to Main", "<<")
    ]),
    "advanced": ("ADVANCED", [
        ("Absolute", "||"),
        ("Percentage", "%"),
        ("Power", "^"),
        ("nth Root", "√"),
        ("Logarithm (Base 10)", "log"),
        ("Logarithm (Base e)", "ln"),
        ("Factorial", "n!"),
        ("History", "?"),
        ("Back to Main", "<<")
    ]),
    "trigonometric": ("TRIGONOMETRIC", [
        ("Sine", "sin"),
        ("Cosine", "cos"),
        ("Tangent", "tan"),
        ("Co-secant", "cosec"),
        ("Secant", "sec"),
        ("Cotangent", "cot"),
        ("History", "?"),
        ("Back to Main", "<<")
    ]),
    "angle_units": ("UNITS OF ANGLE", [
        ("Radian", "rad"),
        ("Degree", "deg"),
        ("Back to Main", "<<")
    ]),
    "programming": ("PROGRAMMING", [
        ("Decimal to Binary", "bin"),
        ("Decimal to Octal", "oct"),
        ("Decimal to Hex", "hex"),
        ("Bitwise AND", "&"),
        ("Bitwise OR", "|"),
        ("Bitwise NOT", "~"),
        ("Logical AND", "&&"),
        ("Logical OR", "||"),
        ("Logical NOT", "!"),
        ("History", "?"),
        ("Back to Main", "<<")
    ])
}


# Displays a menu dynamically
def show_menu(title, options):
    """
    :param title: The title of the menu.
    :param options: A list of tuples containing option text and shortcuts.
    """
    print('\033[36m' + '-' * 31)
    print(f"|{title.center(29)}|")
    print('-' * 31 + '\033[0m')
    print("Select operation.")
    for idx, (desc, shortcut) in enumerate(options, start=1):
        digit = count_digits(idx)
        padding = 21 - digit  # Adjust padding based on the number of digits
        print(f"{idx}. {desc:<{padding}}: {shortcut}")
    print("")


def show_main_menu():
    # title, options = menus["main"]  # Unpack manually
    # show_menu(title, options)  # Pass arguments to the function
    show_menu(*menus["main"])


def show_basic_menu():
    show_menu(*menus["basic"])


def show_advanced_menu():
    show_menu(*menus["advanced"])


def show_trigonometric_menu():
    show_menu(*menus["trigonometric"])


def show_angles_units():
    show_menu(*menus["angle_units"])


def show_programming_menu():
    show_menu(*menus["programming"])


# get number of digits count
def count_digits(num):
    return len(f"{abs(num)}")



# Function to clear the console screen
def clear():
    # Clear the console - 'nt' for Windows and 'posix' for Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')


# Input helper to safely get float input
def input_num(prompt):
    while True:
        num = input(f"{prompt}: ")
        if num.endswith('$'):
            clear()
            return 0

        if num.endswith('#'):
            return -1

        try:
            return float(num)
        except ValueError:
            print("\033[31mInvalid input, please try again.\033[0m")
            continue

# Basic arithmetic operations

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "\033[31mError: Division by zero\033[0m"

def square(a):
    return a ** 2

def square_root(a):
    return math.sqrt(a)

def remainder(a, b):
    return a % b


# Advanced operations

def absolute(a):
    return abs(a)

def percentage(a):
    return a / 100

def nth_root(a, n):
    return a ** (1/n)

def logarithm_base_10(a):
    return math.log10(a)

def logarithm_base_e(a):
    return math.log(a)

def factorial(a):
    return math.factorial(int(a))


# Programming conversion operations

def decimal_to_binary(num):
    return bin(int(num))

def decimal_to_octal(num):
    return oct(int(num))

def decimal_to_hex(num):
    return hex(int(num))

def bitwise_and(a, b):
    return a & b  # Bitwise AND

def bitwise_or(a, b):
    return a | b  # Bitwise OR

def bitwise_not(a):
    return ~a  # Bitwise NOT

def logical_and(a, b):
    return a and b  # Logical AND

def logical_or(a, b):
    return a or b  # Logical OR

def logical_not(a):
    return not a  # Logical NOT


# Show history for each menu

def iterate_cal_list(cal_list):
    if len(cal_list) == 0:
        print("\033[34mNo past calculations to show\033[0m")
    else:
        for cal in cal_list:
            print(cal)

def show_history(menu):
    clear()

    print('\033[36m-------------------------------')
    print('|           HISTORY          |')
    print('-------------------------------\033[0m')

    menu = menu.upper()
    if menu == 'BASIC':
        iterate_cal_list(basic_cal_list)
    elif menu == 'ADVANCED':
        iterate_cal_list(advanced_cal_list)
    elif menu == 'TRIGONOMETRIC':
        iterate_cal_list(trigonometric_cal_list)
    elif menu == 'PROGRAMMING':
        iterate_cal_list(programming_cal_list)

    input("\nPress Enter to go back...")

show_main_menu()
show_basic_menu()
show_advanced_menu()
show_trigonometric_menu()
show_programming_menu()
show_angles_units()
# show_history("basic")

# def select_op(operation):
#     if operation == '#':
#         return -1
#     elif operation == '$':
#         clear()
#         return 0
#     elif operation == '?':
#         show_history()
#         return 0
#     elif operation == 'X':
#         clear()
#         return 0
#     elif operation in ('+', '-', '*', '/', '^', '%'):
#         result = 0.0
#
#         num1 = input_num('first')
#         num2 = input_num('second')
#
#         if operation == '+':
#             result = add(num1, num2)
#         elif operation == '-':
#             result = subtract(num1, num2)
#         elif operation == '*':
#             result = multiply(num1, num2)
#         elif operation == '/':
#             result = divide(num1, num2)
#         elif operation == '^':
#             result = power(num1, num2)
#         elif operation == '%':
#             result = remainder(num1, num2)
#         else:
#             print("\033[31mSomething Went Wrong\033[0m")
#
#         last_calculation = "\033[34m{0} {1} {2} = {3}\033[0m".format(num1, operation, num2, result)
#         print(last_calculation)
#         basic_cal_list.append(last_calculation)
#
#
#     else:
#         print("\033[31mUnrecognized operation\033[0m")
#



# while True:
#     show_main_menu()
#     # take input from the user
#     choice = input("Enter choice(+,-,*,/,^,%,#,$,?): ")
#     if select_op(choice) == -1:
#         # program ends here
#         print("\033[32mDone. Terminating\033[0m")
#         exit()
