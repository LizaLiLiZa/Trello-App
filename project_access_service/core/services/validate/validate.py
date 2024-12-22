"""A class for validating information."""
import re
import datetime

class ValidateInfo():
    """A class for validating information."""

    @staticmethod
    def validation_name(value: str) -> bool:
        """
            Checks whether the name matches the specified patterns for English or Russian letters.

            The name must begin with a capital letter, followed by lowercase letters.
            The length of the name can be from 2 to 201 characters (including the first letter).

            Args:
                value (str): The name to check.

            Returns:
                bool: True if the name meets the requirements, otherwise False.
        """
        pattern_en = r"^[A-Z]{1}[a-z]{1,200}$"
        pattern_rus = r"^[А-Я]{1}[а-я]{1,200}$"
        if re.match(pattern_en, value) or re.match(pattern_rus, value):
            return True
        return False

    @staticmethod
    def validation_birthday_at(value: datetime.date) -> bool:
        """
            Checks if the user is 12 years old.

            Args:
                value (datetime.date): Date of birth.

            Returns:
                bool: True if the date of birth meets the requirements, otherwise False.
        """
        date_min = datetime.date(datetime.datetime.now().year - 12, datetime.datetime.now().month, datetime.datetime.now().day)
        date_max = datetime.date(datetime.datetime.now().year - 120, datetime.datetime.now().month, datetime.datetime.now().day)
        if value <= date_min and value >= date_max:
            return True
        return False

    @staticmethod
    def validate_phone(value: str) -> bool:
        """
            Checks whether the number matches the specified pattern.

            The number should consist of 7-15 digits.

            Args:
                value (int): The phone number for verification.

            Returns:
                bool: True if the phone meets the requirements, otherwise False.
        """
        pattern = r"^[0-9]{7,15}$"
        if re.match(pattern, value):
            return True
        return False

    @staticmethod
    def validate_password(value: str) -> bool:
        """
            Checks whether the phone matches the specified pattern.

            The number should consist of 7-15 digits.

            Args:
                value (int): The phone number for verification.

            Returns:
                bool: True if the phone meets the requirements, otherwise False.
        """
        pattern = r"^[a-zA-Zа-яА-Я0-9,./*-_=+]{8,16}$"
        if re.match(pattern, value):
            return True
        return False
