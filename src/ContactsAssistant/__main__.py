"""Main App"""

from constants import INPUT_STYLE
from handler import Handler
from menu import Menu
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

handler = Handler()


def parse_input(user_input):
    """
    Parse user input into a command and its arguments.

    Args:
        user_input (str): The input string from the user.

    Returns:
        tuple: The command and a list of arguments.
    """
    cmd, *args = user_input.split()
    cmd = Menu.get_by_name(cmd)
    return cmd, *args


def main():
    """
    Main function to run the assistant bot.

    Continuously prompts the user for commands and executes the appropriate function.
    """
    print(handler.greeting())
    while True:
        style = Style.from_dict(INPUT_STYLE)
        user_input = prompt(
            "Enter a command >>> ", completer=handler.completer, style=style
        )
        command, *args = parse_input(user_input)
        print(handler.execute(command, args))
        print()
        if command in (Menu.EXIT, Menu.CLOSE):
            break
        print()


if __name__ == "__main__":
    main()
