import os
import math

# History lists for each menu
history = {
    "basic": [],
    "advanced": [],
    "trigonometric": [],
    "programming": []
}

is_known_choice = True

# Angle unit is degree by default
is_degree = True

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
        ("Square Root", "root"),
        ("Remainder", "mod"),
        ("History", "?"),
        ("Reset", "$"),
        ("Back to Main", "<<")
    ]),
    "advanced": ("ADVANCED", [
        ("Absolute", "||"),
        ("Percentage", "%"),
        ("Power", "^"),
        ("nth Root", "root"),
        ("Logarithm (Base 10)", "log"),
        ("Logarithm (Base e)", "ln"),
        ("Factorial", "n!"),
        ("History", "?"),
        ("Reset", "$"),
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
        ("Reset", "$"),
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
        ("Reset", "$"),
        ("Back to Main", "<<")
    ])
}


# Displays a menu dynamically
def show_menu(menu_name):
    global is_known_choice

    while True:
        # title: The title of the menu.
        # options: A list of tuples containing option text and shortcuts.
        title, options = menus[menu_name]

        print('\033[36m' + '-' * 38)
        print(f"|{title.center(36)}|")
        print('-' * 38 + '\033[0m')
        print("Select operation.")

        for idx, (desc, shortcut) in enumerate(options, start=1):
            # Adjust padding based on the number of digits
            digit = count_digits(idx)
            padding = 21 - digit
            print(f"{idx}. {desc:<{padding}}: {shortcut}")


        is_known_choice = True
        handle_menu_input(menu_name, options)


# Handle menu input
def handle_menu_input(menu_name, options):
    global is_known_choice

    shortcuts = {shortcut: desc for desc, shortcut in options}
    while is_known_choice:
        choice = input(f"Enter choice ({', '.join(shortcuts.keys())}): ").strip()
        if choice in shortcuts:
            if choice == "#":
                print("\033[32mDone. Terminating\033[0m")
                exit()
            elif choice == "<<":
                clear()
                show_menu("main")
                return
            elif choice == "$":
                clear()
                history[menu_name] = []
                show_menu(menu_name)
            elif choice == "?":
                clear()
                show_history(menu_name)
            else:
                if menu_name == "main":
                    clear()
                    navigate_to_sub_menus(choice)
                elif menu_name == "angle_units":
                    clear()
                    select_angle_unit(choice)
                else:
                    perform_operation(menu_name, choice)
        else:
            print("\033[31mUnrecognized choice, try again.\033[0m")




# navigate to sub menus
def navigate_to_sub_menus(menu):
    if menu == 'BAS':
        show_menu('basic')
    elif menu == 'ADV':
        show_menu('advanced')
    elif menu == 'TRI':
        show_menu('angle_units')
    elif menu == 'PRO':
        show_menu('programming')


def select_angle_unit(unit):
    global is_degree  # Declare is_degree as global

    if unit == "rad":
        is_degree = False

    show_menu('trigonometric')


# Perform operations
def perform_operation(menu_name, operation):
    global is_known_choice

    num1 = get_number("Enter first number")

    if menu_name == "basic" and operation not in ["^", "root"]:
        num2 = get_number("Enter second number")
    elif menu_name == "advanced" and operation not in ["||", "%", "log", "ln", "n!"]:
        num2 = get_number("Enter second number")
    elif menu_name == "programming" and operation not in ["bin", "oct", "hex", "~", "!"]:
        num2 = get_number("Enter second number")
    else:
        num2 = None

    result = calculate(menu_name, operation, num1, num2)

    print(f"\033[34mResult: {result}\033[0m")
    last_calculation = "\033[34m{0} {1} {2} = {3}\033[0m".format(num1, operation, num2 if num2 is not None else '',
                                                                 result)
    # history[menu_name].append(f"{num1} {operation} {num2 if num2 is not None else ''} = {result}")
    history[menu_name].append(last_calculation)

    input("\nPress Enter to go next calculation...")
    is_known_choice = False
    clear()


# Perform calculations
def calculate(menu, operation, num1, num2):
    if menu == "basic":
        operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b if b != 0 else "\033[31mError: Division by zero\033[0m",
            "^": lambda a, _: a ** 2,
            "root": lambda a, _: math.sqrt(a),
            "mod": lambda a, b: a % b
        }
    elif menu == "advanced":
        operations = {
            "||": lambda a, _: abs(a),
            "%": lambda a, _: a / 100,
            "^": lambda a, b: a ** b,
            "root": lambda a, b: a ** (1 / b),
            "log": lambda a, _: math.log10(a),
            "ln": lambda a, _: math.log(a),
            "n!": lambda a, _: math.factorial(int(a))
        }
    elif menu == "trigonometric":
        angle_convert = math.radians if is_degree else lambda x: x
        operations = {
            "sin": lambda a, _: math.sin(angle_convert(a)),
            "cos": lambda a, _: math.cos(angle_convert(a)),
            "tan": lambda a, _: math.tan(angle_convert(a)),
            "cosec": lambda a, _: 1 / math.sin(angle_convert(a)),
            "sec": lambda a, _: 1 / math.cos(angle_convert(a)),
            "cot": lambda a, _: 1 / math.tan(angle_convert(a)) if math.tan(angle_convert(a)) != 0 else float('inf')
        }
    elif menu == "programming":
        operations = {
            "bin": lambda a, _: bin(int(a)),
            "oct": lambda a, _: oct(int(a)),
            "hex": lambda a, _: hex(int(a)),
            "&": lambda a, b: int(a) & int(b),
            "|": lambda a, b: int(a) | int(b),
            "~": lambda a, _: ~int(a),
            "&&": lambda a, b: bool(a) and bool(b),
            "||": lambda a, b: bool(a) or bool(b),
            "!": lambda a, _: not bool(a)
        }
    else:
        raise ValueError("Unsupported menu")

    return operations[operation](num1,num2)


# Show history
def show_history(menu):
    global is_known_choice
    print('\033[36m' + '-' * 38)
    print(f"|{f'HISTORY OF {menu.upper()} MENU'.center(36)}|")
    print('-' * 38 + '\033[0m')

    if not history[menu]:
        print("\033[34mNo past calculations to show\033[0m")
    else:
        for entry in history[menu]:
            print(entry)
    input("\nPress Enter to go back...")
    is_known_choice = False


# Get number input
def get_number(prompt):
    while True:
        try:
            return float(input(f"{prompt}: "))
        except ValueError:
            print("\033[31mInvalid number. Try again.\033[0m")


# Clear screen
def clear():
    # Clear the console - 'nt' for Windows and 'posix' for Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')


# get number of digits count
def count_digits(num):
    return len(f"{abs(num)}")


# Main execution
if __name__ == "__main__":
    clear()
    show_menu("main")
