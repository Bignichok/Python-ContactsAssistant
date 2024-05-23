"""Class Menu module"""

import difflib
from enum import Enum
from collections import namedtuple
from constants import MENU_BORDER
from utils import format_cmd, format_param

Item = namedtuple('Item', ['min_required_params', 'param_list', 'hint'])

class Menu(Enum):
    '''Class'''
    HELLO                   = Item(0, [], 'to show command list')
    ADD_CONTACT             = Item(2, ['CONTACT_NAME', 'PHONE', 'EMAIL'], 'to add a new contact')
    UPDATE_CONTACT          = Item(3, ['CONTACT_NAME','OLD PHONE','NEW PHONE'], 'to update a phone')
    DELETE_CONTACT          = Item(1, ['CONTACT_NAME'], 'to delete contact')
    SET_CONTACT_BIRTHDAY    = Item(2, ['CONTACT_NAME','BIRTHDAY DATE'], 'to set birthday')
    GET_CONTACT_BIRTHDAY    = Item(1, ['CONTACT_NAME'], 'to show birthday')
    GET_CONTACT_BY_NAME     = Item(1, ['CONTACT_NAME'], 'to find a contact by name')
    GET_CONTACT_BY_PHONE    = Item(1, ["PHONE"], 'text": "to find a contact by phone')
    GET_CONTACT_BY_EMAIL    = Item(1, ["EMAIL"], 'text": "to find a contact by email')
    GET_ALL_CONTACTS        = Item(0, [], 'to view a full contact list')
    GET_UPCOMING_BIRTHDAYS  = Item(0, [], 'to show all birthdays in this week')
    UPDATE_CONTACT_EMAIL    = Item(2, ['CONTACT_NAME', 'EMAIL'], 'to update email')
    NOTE_ADD                = Item(2, ['NOTE_SUBJECT','NOTE_TEXT'], 'to add or update note')
    NOTE_DEL                = Item(1, ['NOTE_SUBJECT'], 'to delete note')
    NOTE_TAG                = Item(2, ['NOTE_SUBJECT','TAG'], 'to add tag to note')
    NOTE_TAG_DEL            = Item(2, ['NOTE_SUBJECT','TAG'], 'to delete note tag')
    NOTE_ALL                = Item(0, [], 'to view a full note list')
    EXIT                    = Item(0, [], 'to app close')
    CLOSE                   = Item(0, [], 'to app close')

    @classmethod
    def pretty_print(cls):
        """Print all menu items"""
        res = ""
        res += MENU_BORDER
        for k, v in {x.name.lower():x.value for x in cls}.items():        
            res += f'[x] {format_cmd(k)} '
            res += f'{format_param(' '.join([f'[{x}]' for x in v.param_list]))} '
            res += f'{v.hint}\n'
        res += MENU_BORDER
        return res

    @classmethod
    def get_commands_list(cls) -> list:
        """Return all keys"""
        return [x.name.lower() for x in cls]

    @classmethod
    def get_by_name(cls, name: str) -> list:
        '''Return all keys'''
        return {x.name.lower().strip() : x for x in cls}.get(name.lower().strip())

    @classmethod
    def check_params(cls, command, args: list) -> str:
        '''Return all keys'''
        row = cls(command)
        min = row.value[0]
        max = len(row.value[1])
        if not min <= len(args) <= max:
            raise ValueError(f'This command requires {min} to {max} parameters {row.value[1]}')
    
    @classmethod
    def get_commands_witn_args(cls) -> dict:
        """Return all commands with params"""
        commands = {x.name.lower().strip() : x.value[1] for x in cls}
        return commands

    @staticmethod
    def suggest_similar_commands(input_command):
        """
        Suggests similar commands based on user input command.
        """
        available_commands = Menu.get_commands_list()
        similar_commands = difflib.get_close_matches(input_command, available_commands)
        return similar_commands
