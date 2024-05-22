"""Class Menu module"""

from enum import Enum
from constants import MENU_BORDER
from utils import format_cmd, format_param


class Menu(Enum):
    """Class"""

    HELLO = {"p": [], "text": "to show command list"}
    ADD_CONTACT = {
        "p": ["CONTACT_NAME", "PHONE", "EMAIL"],
        "text": "to add a new contact",
    }
    UPDATE_CONTACT = {
        "p": ["CONTACT_NAME", "OLD PHONE", "NEW PHONE"],
        "text": "to update a phone",
    }
    DELETE_CONTACT = {"p": ["CONTACT_NAME"], "text": "to delete contact"}
    SET_CONTACT_BIRTHDAY = {
        "p": ["CONTACT_NAME", "BIRTHDAY DATE"],
        "text": "to set birthday",
    }
    GET_CONTACT_BIRTHDAY = {"p": ["CONTACT_NAME"], "text": "to show birthday"}
    GET_CONTACT = {"p": ["CONTACT_NAME"], "text": "to find a contact by name"}
    GET_ALL_CONTACTS = {"p": [], "text": "to view a full contact list"}
    GET_UPCOMING_BIRTHDAYS = {"p": [], "text": "to show all birthdays in this week"}
    UPDATE_CONTACT_EMAIL = {"p": ["CONTACT_NAME", "EMAIL"], "text": "to update email"}
    NOTE_ADD = {"p": ["NOTE_SUBJECT", "NOTE_TEXT"], "text": "to add or update note"}
    NOTE_DEL = {"p": ["NOTE_SUBJECT"], "text": "to delete note"}
    NOTE_TAG = {"p": ["NOTE_SUBJECT", "TAG"], "text": "to add tag to note"}
    NOTE_TAG_DEL = {"p": ["NOTE_SUBJECT", "TAG"], "text": "to delete note tag"}
    NOTE_ALL = {"p": [], "text": "to view a full note list"}
    EXIT = {"p": [], "text": "to app close"}
    CLOSE = {"p": [], "text": "to app close"}

    @classmethod
    def pretty_print(cls):
        """Print all menu items"""
        res = ""
        res += MENU_BORDER
        for k, v in {x.name.lower(): x.value for x in cls}.items():
            res += f"[x] {format_cmd(k)} "
            res += f"{format_param(' '.join([f'[{x}]' for x in v.get('p')]))} "
            res += f"{v.get('text')}\n"
        res += MENU_BORDER
        return res

    @classmethod
    def get_commands_list(cls) -> list:
        """Return all keys"""
        return [x.name.lower() for x in cls]
