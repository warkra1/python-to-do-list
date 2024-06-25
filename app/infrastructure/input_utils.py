def ask_number(message: str) -> int:
    while True:
        number_str = input(message)
        if number_str.isdigit():
            return int(number_str)

        print("Invalid number!")
