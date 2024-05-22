'''Class Menu module'''
from enum import Enum
from constants import MENU_BORDER
from utils import format_cmd, format_param

class Menu(Enum):
    '''Class'''
    HELLO                = {'p' : [],                                         'text' : 'to show command list'}
    CONTACT_ADD          = {'p' : ['CONTACT_NAME','PHONE'],                   'text' : 'to add a new contact'}
    CONTACT_UPD          = {'p' : ['CONTACT_NAME','OLD PHONE','NEW PHONE'],   'text' : 'to update a phone'}
    CONTACT_DEL          = {'p' : ['CONTACT_NAME'],                           'text' : 'to delete contact'}
    CONTACT_SET_BIRTHDAY = {'p' : ['CONTACT_NAME','BIRTHDAY'],                'text' : 'to set birthday'}
    CONTACT_BIRTHDAY     = {'p' : ['CONTACT_NAME'],                           'text' : 'to show birthday'}
    CONTACT_PHONE        = {'p' : ['CONTACT_NAME'],                           'text' : 'to find a phone by name'}
    CONTACT_ALL          = {'p' : [],                                         'text' : 'to view a full contact list'}
    BIRTHDAYS            = {'p' : ['CONTACT_NAME'],                           'text' : 'to show all birthdays in this week'}
    NOTE_ADD             = {'p' : ['NOTE_SUBJECT','NOTE_TEXT'],               'text' : 'to add or update note'}
    NOTE_DEL             = {'p' : ['NOTE_SUBJECT'],                           'text' : 'to delete note'}
    NOTE_TAG             = {'p' : ['NOTE_SUBJECT','TAG'],                     'text' : 'to add tag to note'}
    NOTE_TAG_DEL         = {'p' : ['NOTE_SUBJECT','TAG'],                     'text' : 'to delete note tag'}
    NOTE_ALL             = {'p' : [],                                         'text' : 'to view a full note list'}
    EXIT                 = {'p' : [],                                         'text' : 'to app close'}
    CLOSE                = {'p' : [],                                         'text' : 'to app close'}

    @classmethod
    def pretty_print(cls):
        '''Print all menu items'''
        res = ''
        res += MENU_BORDER
        for k, v in {x.name.lower():x.value for x in cls}.items():        
            res += f'[x] {format_cmd(k)} '
            res += f'{format_param(' '.join([f'[{x}]' for x in v.get('p')]))} '
            res += f'{v.get('text')}\n'
        res += MENU_BORDER
        return res

    @classmethod
    def get_commands_list(cls) -> list:
        '''Return all keys'''
        return [x.name.lower() for x in cls]
