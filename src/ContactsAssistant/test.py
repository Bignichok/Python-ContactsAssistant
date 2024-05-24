from datetime import date, timedelta
import random
import unittest
from argparse import Namespace
from handler import Handler
from menu import Menu
from constants import DATE_FORMAT


class TestHandler(unittest.TestCase):
    """
    Test cases for the Handler class.
    """

    def setUp(self):
        """
        Set up a new Handler instance and clear the contact book before each test.
        """
        self.handler = Handler()
        self.handler.contact_book.clear()

    def test_add_contact(self):
        """
        Test adding a new contact.
        """
        args = Namespace(
            name="Stepan Bandera",
            phone="1234567890",
            email="bandera@ukr.net",
            birthday="01.01.1980",
        )
        result = self.handler.execute(Menu.ADD_CONTACT, args)
        self.assertEqual(result, "Contact added.")

        # Verify contact was added
        find_args = Namespace(
            name="Stepan Bandera", phone=None, email=None, birthday=None
        )
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_NAME, find_args)
        self.assertIn("Stepan Bandera", str(contact))

    def test_delete_contact(self):
        """
        Test deleting an existing contact.
        """
        # Add a contact to delete
        add_args = Namespace(
            name="Stepan Bandera",
            phone="1234567890",
            email="bandera@ukr.net",
            birthday="01.01.1980",
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Delete the contact
        delete_args = Namespace(
            name="Stepan Bandera", phone=None, email=None, birthday=None
        )
        result = self.handler.execute(Menu.DELETE_CONTACT, delete_args)
        self.assertEqual(result, "Contact removed.")

        # Verify contact was deleted
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_NAME, delete_args)
        self.assertEqual(contact, "Contact does not exist, you can add it")

    def test_update_phone(self):
        """
        Test updating the phone number of an existing contact.
        """
        # Add a contact to update
        add_args = Namespace(
            name="Stepan Bandera",
            phone="1234567890",
            email="bandera@ukr.net",
            birthday="01.01.1980",
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Update phone number
        update_args = Namespace(
            name="Stepan Bandera",
            oldphone="1234567890",
            newphone="0987654321",
            phone=None,
            email=None,
            birthday=None,
        )
        result = self.handler.execute(Menu.UPDATE_PHONE, update_args)
        self.assertEqual(result, "Phone changed")

        # Verify phone number was updated
        find_args = Namespace(
            name="Stepan Bandera", phone=None, email=None, birthday=None
        )
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_NAME, find_args)
        self.assertIn("0987654321", str(contact))

    def test_set_contact_birthday(self):
        """
        Test setting the birthday for an existing contact.
        """
        # Add a contact to update
        add_args = Namespace(
            name="Stepan Bandera", phone="1234567890", email=None, birthday=None
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Set birthday
        birthday_args = Namespace(
            name="Stepan Bandera", birthday="01.01.1980", phone=None, email=None
        )
        result = self.handler.execute(Menu.SET_BIRTHDAY, birthday_args)
        self.assertEqual(result, "Birthday added.")

        # Verify birthday was set
        find_args = Namespace(
            name="Stepan Bandera", phone=None, email=None, birthday=None
        )
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_NAME, find_args)
        self.assertIn("01.01.1980", str(contact))

    def test_get_contact_birthday(self):
        """
        Test retrieving the birthday of an existing contact.
        """
        # Add a contact with a birthday
        add_args = Namespace(
            name="Stepan Bandera",
            phone="1234567890",
            email="bandera@ukr.net",
            birthday="01.01.1980",
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Get birthday
        find_args = Namespace(
            name="Stepan Bandera", phone=None, email=None, birthday=None
        )
        birthday = self.handler.execute(Menu.SHOW_BIRTHDAY, find_args)
        self.assertEqual(str(birthday), "01.01.1980")

    def test_get_upcoming_birthdays(self):
        """
        Test retrieving contacts with upcoming birthdays.
        """
        # Add a contact with a birthday
        add_args = Namespace(
            name="Stepan Bandera",
            phone="1234567890",
            email="bandera@ukr.net",
            birthday=(date.today() + timedelta(random.randint(1, 25))).strftime(
                DATE_FORMAT
            ),
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Get upcoming birthdays within next 30 days
        upcoming_args = Namespace(
            days=30, name=None, phone=None, email=None, birthday=None
        )
        result = self.handler.execute(Menu.UPCOMING_BIRTHDAYS, upcoming_args)
        self.assertIn("Stepan Bandera", result)

    def test_update_contact_email(self):
        """
        Test updating the email address of an existing contact.
        """
        # Add a contact to update
        add_args = Namespace(
            name="Stepan Bandera",
            phone="1234567890",
            email="bandera@ukr.net",
            birthday="01.01.1980",
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Update email
        update_email_args = Namespace(
            name="Stepan Bandera",
            email="new_email@example.com",
        )
        result = self.handler.execute(Menu.UPDATE_EMAIL, update_email_args)
        self.assertEqual(result, "Email changed")

        # Verify email was updated
        find_args = Namespace(
            name="Stepan Bandera", phone=None, email=None, birthday=None
        )
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_NAME, find_args)
        self.assertIn("new_email@example.com", str(contact))

    def test_add_address(self):
        """
        Test adding an address to an existing contact.
        """
        # Add a contact to update
        add_args = Namespace(
            name="Stepan Bandera", phone="1234567890", email=None, birthday=None
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Verify the contact exists
        find_args = Namespace(
            name="Stepan Bandera", phone=None, email=None, birthday=None
        )
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_NAME, find_args)

        # Add address
        address_args = Namespace(
            name="Stepan Bandera",
            addresstype="Home",
            street="vulytsia Natsionalistiv 3",
            city="Staryi Uhryniv",
            postalcode="77362",
            country="Ukraine",
        )
        result = self.handler.execute(Menu.ADD_ADDRESS, address_args)
        self.assertEqual(result, "Address added.")

        # Verify address was added
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_NAME, find_args)
        self.assertIn("vulytsia Natsionalistiv 3", str(contact))

    def test_remove_address(self):
        """
        Test removing an address from an existing contact.
        """
        # Add a contact with an address
        add_args = Namespace(
            name="Stepan Bandera", phone="1234567890", email=None, birthday=None
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Add address
        address_args = Namespace(
            name="Stepan Bandera",
            addresstype="Home",
            street="vulytsia Natsionalistiv 3",
            city="Staryi Uhryniv",
            postalcode="77362",
            country="Ukraine",
        )
        self.handler.execute(Menu.ADD_ADDRESS, address_args)

        # Verify the address was added
        find_args = Namespace(
            name="Stepan Bandera", phone=None, email=None, birthday=None
        )
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_NAME, find_args)

        # Remove address
        remove_address_args = Namespace(
            name="Stepan Bandera",
            addresstype="Home",
        )
        result = self.handler.execute(Menu.REMOVE_ADDRESS, remove_address_args)
        self.assertEqual(result, "Address removed.")

        # Verify address was removed
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_NAME, find_args)
        self.assertNotIn("vulytsia Natsionalistiv 3", str(contact))

    def test_get_contact_by_phone(self):
        """
        Test retrieving a contact by their phone number.
        """
        # Add a contact
        add_args = Namespace(
            name="Stepan Bandera", phone="1234567890", email=None, birthday=None
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Find contact by phone
        find_args = Namespace(name=None, phone="1234567890", email=None, birthday=None)
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_PHONE, find_args)
        self.assertIn("Stepan Bandera", str(contact))

    def test_get_contact_by_email(self):
        """
        Test retrieving a contact by their email address.
        """
        # Add a contact
        add_args = Namespace(
            name="Stepan Bandera",
            phone="1234567890",
            email="bandera@ukr.net",
            birthday=None,
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Find contact by email
        find_args = Namespace(
            name=None, phone=None, email="bandera@ukr.net", birthday=None
        )
        contact = self.handler.execute(Menu.FIND_CONTACT_BY_EMAIL, find_args)
        self.assertIn("Stepan Bandera", str(contact))

    def test_show_all_contacts(self):
        """
        Test showing all contacts.
        """
        # Add a contact
        add_args = Namespace(
            name="Stepan Bandera", phone="1234567890", email=None, birthday=None
        )
        self.handler.execute(Menu.ADD_CONTACT, add_args)

        # Show all contacts
        result = self.handler.execute(Menu.SHOW_ALL_CONTACTS, None)
        self.assertIn("Stepan Bandera", result)

    def test_show_commands(self):
        """
        Test showing all available commands.
        """
        # Show available commands
        result = self.handler.execute(Menu.SHOW_COMMANDS, None)
        self.assertIn("Add a new contact", result)

    def test_exit(self):
        """
        Test exit command.
        """
        result = self.handler.execute(Menu.EXIT, None)
        self.assertEqual(result, "Good bye!")

    def test_close(self):
        """
        Test close command.
        """
        result = self.handler.execute(Menu.CLOSE, None)
        self.assertEqual(result, "Good bye!")


if __name__ == "__main__":
    unittest.main()
