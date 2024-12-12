import os
import math

# History lists for each menu
history = {
    "basic": [],
    "advanced": [],
    "trigonometric": [],
    "programming": []
}

is_exist_menu = True

# Angle unit is degree by default
is_degree = True

# Define menus dictionary
menus = {
    "main": ("WELCOME!", [
        ("Basic", "BAS"),
        ("Advanced", "ADV"),
        ("Trigonometric", "TRI"),
        ("Programming", "PRO"),
        ("Reset", "$"),
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
        ("Back to Units", "<"),
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

# Define operations that require only one number for each menu
single_number_operations = {
    "basic": ["^", "root"],
    "advanced": ["||", "%", "log", "ln", "n!"],
    "trigonometric": ["sin", "cos", "tan", "cosec", "sec", "cot"],
    "programming": ["bin", "oct", "hex", "~", "!"]
}


# Displays a menu dynamically
def show_menu(menu_name):
    global is_exist_menu

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
            print(f"\033[34m{idx}. {desc:<{padding}}: {shortcut}\033[0m")

        is_exist_menu = True
        handle_menu_input(menu_name, options)


# Handle menu input
def handle_menu_input(menu_name, options):
    global is_exist_menu

    shortcuts = {shortcut: desc for desc, shortcut in options}

    while is_exist_menu:
        choice = input(f"Enter choice ({', '.join(shortcuts.keys())}): ").strip()
        if choice in shortcuts:
            if choice == "#":
                print("\033[32mDone. Terminating\033[0m")
                exit()
            elif choice == "<":
                clear()
                show_menu("angle_units")
            elif choice == "<<":
                clear()
                show_menu("main")
            elif choice == "$":
                reset(menu_name)
            elif choice == "?":
                clear()
                show_history(menu_name)
            else:
                if menu_name == "main":
                    clear()
                    navigate_to_sub_menus(choice, shortcuts)
                elif menu_name == "angle_units":
                    clear()
                    select_angle_unit(choice)
                else:
                    perform_operation(menu_name, choice)
        else:
            print("\033[31mUnrecognized choice, try again.\033[0m")


# navigate to sub menus
def navigate_to_sub_menus(menu, sub_menus):
    sub_menus["TRI"] = "angle_units"

    # return "main" as a fallback.
    show_menu(sub_menus.get(menu, "main").lower())


def select_angle_unit(unit):
    global is_degree  # Declare is_degree as global

    if unit == "rad":
        is_degree = False
    elif unit == "deg":
        is_degree = True

    show_menu('trigonometric')


# Perform operations
def perform_operation(menu_name, operation):
    global is_exist_menu

    num1, num2 = get_numbers(menu_name, operation)
    result = calculate(menu_name, operation, num1, num2)

    if num2 is None:
        if operation in single_number_operations.get('basic', []):
            if operation == '^':
                last_calculation = "\033[32m{0} {1} {2} = {3}\033[0m".format(num1, operation, 2, result)
            elif operation == 'root':
                last_calculation = "\033[32m{0} {1} {2} = {3}\033[0m".format(2, "\u221A", num1, result)
        elif operation in single_number_operations.get('advanced', []):
            if operation == '||':
                last_calculation = "\033[32m|{0}| = {1}\033[0m".format(num1, result)
            elif operation == '%':
                last_calculation = "\033[32m{0} {1} = {2}\033[0m".format(num1, operation, result)
            elif operation == 'n!':
                last_calculation = "\033[32m{0}! = {1}\033[0m".format(num1, result)
            else:
                last_calculation = "\033[32m{0}({1}) = {2}\033[0m".format(operation, num1, result)
        elif operation in single_number_operations.get('trigonometric', []):
            last_calculation = "\033[32m{0}({1} {2}) = {3}\033[0m".format(operation, num1,
                                                                          'deg' if is_degree else 'rad', result)
        elif operation in single_number_operations.get('programming', []):
            last_calculation = "\033[32m{0} {1} = {2}\033[0m".format(operation, num1, result)

    elif operation == '/' or operation == 'mod':
        last_calculation = "\033[32m{0} {1} {2} {3} {4}\033[0m".format(num1, '/' if operation == '/' else '%', num2,
                                                                       ' ' if isinstance(result, str) else "=", result)
    elif operation == 'root':
        last_calculation = "\033[32m{0} {1} {2} = {3}\033[0m".format(num2, "\u221A", num1, result)
    else:
        last_calculation = "\033[32m{0} {1} {2} = {3}\033[0m".format(num1, operation, num2, result)

    print(last_calculation)

    history[menu_name].append(last_calculation)

    input("\nPress Enter to go next calculation...")
    is_exist_menu = False
    clear()


# Perform calculations
def calculate(menu, operation, num1, num2):
    if menu == "basic":
        operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: divide(a, b),
            "^": lambda a, _: a ** 2,
            "root": lambda a, _: math.sqrt(a),
            "mod": lambda a, b: modulus(a, b)
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

    return operations[operation](num1, num2)


def divide(a, b):
    if b == 0:
        return "\033[31mError: Division by zero\033[0m"

    result = a / b

    if result.is_integer():
        return int(result)

    return result


def modulus(a, b):
    if b == 0:
        return "\033[31mError: modulo by zero\033[0m"

    if isinstance(a, int) and isinstance(b, int):
        return a % b
    else:
        return math.fmod(a,b)


# Show history
def show_history(menu):
    global is_exist_menu
    print('\033[36m' + '-' * 38)
    print(f"|{f'HISTORY OF {menu.upper()} MENU'.center(36)}|")
    print('-' * 38 + '\033[0m')

    if not history[menu]:
        print("\033[34mNo past calculations to show\033[0m")
    else:
        for entry in history[menu]:
            print(entry)
    input("\nPress Enter to go back...")
    is_exist_menu = False
    clear()


# get operands (numbers)
def get_number(prompt):
    while True:
        num = input(f"{prompt}: ")

        # reset during taking operands
        if num == '$':
            return '$'

        try:
            return int(num)
        except ValueError:
            try:
                return float(num)
            except ValueError:
                print("\033[31mInvalid number. Try again.\033[0m")


def get_numbers(menu_name, operation):
    # Check if the operation requires a single number
    if operation in single_number_operations.get(menu_name, []):
        num1 = get_number("Enter the number")

        if num1 == '$':
            reset(menu_name)

        return num1, None
    else:
        num1 = get_number("Enter first number")

        if num1 == '$':
            reset(menu_name)

        num2 = get_number("Enter second number")

        if num2 == '$':
            reset(menu_name)

        return num1, num2


# Clear screen
def clear():
    # Clear the console - 'nt' for Windows and 'posix' for Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')


# get number of digits count
def count_digits(num):
    return len(f"{abs(num)}")


# discontinue the current calculation and go new calculation
def reset(menu_name):
    clear()
    show_menu(menu_name)


# Main execution
if __name__ == "__main__":
    clear()
    show_menu("main")
