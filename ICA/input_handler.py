# TODO: Add doc string at class level and method level

class InputHandler:
    @staticmethod
    def get_integer_input(prompt: str) -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid integer")

    
    @staticmethod
    def get_year_input(prompt: str) -> str:
        while True:
            user_input = input(prompt)
            if len(user_input) == 4 and user_input.isdigit():
                return user_input
            print("Invlaid input. Enter a year as 4 digits i.e 2020")