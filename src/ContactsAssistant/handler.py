'''Handler module'''
from constants import GREETING_BANNER
from menu import Menu
from utils import format_greeting

class Handler():
    '''Class'''

    def __init__(self) -> None:
        pass

    def greeting(self) -> str:
        '''Print greeting message'''
        res = f'{format_greeting(GREETING_BANNER)}\n'
        res += f'Welcome to the assistant bot!\n{Menu.pretty_print()}'
        return res

    def hello(self) -> str:
        '''Print hello message'''
        return f"How can I help you? \n{Menu.pretty_print()}"
