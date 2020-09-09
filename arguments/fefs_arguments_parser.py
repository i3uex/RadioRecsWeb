import logging
import re
from collections import namedtuple

REGULAR_EXPRESSION = r"([a-zA-Z_]+)(=)(([a-zA-Z0-9_]+)|(\[(.)+\]))"
"""
Any character string, immediately followed by the equals sign, followed by
either:
- a character string that can include numbers, or even be composed only by
numbers.
- anything between square brackets, in the hopes is correctly written as an
array

This regular expression could match, for example, something like:

- argument=value
- argument=7
- argument=[1, 2, 3]
"""

ArgumentDescriptor = namedtuple("ArgumentDescriptor", ["key", "default_value"])
"""
Tuple describing arguments: its key and a default value, in case that key is
not present.
"""


class ArgumentsParser:
    """
    Manages a list of arguments stored in a dictionary. The key is the name of
    the argument, the value is the value of the argument.
    """
    arguments = {}

    def __init__(self, arguments: dict):
        """
        Creates a new instance of the class with the dictionary of arguments
        provided

        Parameters:
            arguments (dict): Dictionary of arguments to keep track of
        Returns:
            arguments_parser(ArgumentParser): New instance of class
        """
        logging.debug(f"ArgumentsParser.__init__({arguments})")
        self.arguments = arguments

    def get(self, argument_descriptor: ArgumentDescriptor) -> str:
        """
        Given the argument descriptor provided, tries to get the value
        associated with it. If not present, returns the default value included
        in the argument descriptor

        Parameters:
            argument_descriptor (ArgumentDescriptor): descriptor of the
            argument which value is needed.
        Returns:
            value(str): The value associated with the key present in the
            descriptor, the default value present in the descriptor if not
            found
        """
        logging.debug(f"ArgumentsParser.get(\"{argument_descriptor}\")")
        if argument_descriptor.key in self.arguments:
            value = self.arguments[argument_descriptor.key]
        else:
            value = argument_descriptor.default_value
        return value

    def get_bool(self, argument_descriptor: ArgumentDescriptor) -> bool:
        """
        Given the argument descriptor provided, tries to get the value
        associated with it. If not present, returns the default value included
        in the argument descriptor

        Parameters:
            argument_descriptor (ArgumentDescriptor): descriptor of the
            argument which value is needed.
        Returns:
            value(bool): The value associated with the key present in the
            descriptor, the default value present in the descriptor if not
            found, casted to a bool
        """
        logging.debug(f"ArgumentsParser.get_bool(\"{argument_descriptor}\")")
        value = self.get(argument_descriptor)
        return bool(value)

    def get_int(self, argument_descriptor: ArgumentDescriptor) -> int:
        """
        Given the argument descriptor provided, tries to get the value
        associated with it. If not present, returns the default value included
        in the argument descriptor

        Parameters:
            argument_descriptor (ArgumentDescriptor): descriptor of the
            argument which value is needed.
        Returns:
            value(str): The value associated with the key present in the
            descriptor, the default value present in the descriptor if not
            found, casted to an int
        """
        logging.debug(f"ArgumentsParser.get_int(\"{argument_descriptor}\")")
        value = self.get(argument_descriptor)
        return int(value)

    def get_float(self, argument_descriptor: ArgumentDescriptor) -> float:
        """
        Given the argument descriptor provided, tries to get the value
        associated with it. If not present, returns the default value included
        in the argument descriptor

        Parameters:
            argument_descriptor (ArgumentDescriptor): descriptor of the
            argument which value is needed.
        Returns:
            value(str): The value associated with the key present in the
            descriptor, the default value present in the descriptor if not
            found, casted to a float
        """
        logging.debug(f"ArgumentsParser.get_float(\"{argument_descriptor}\")")
        value = self.get(argument_descriptor)
        return float(value)

    def get_list(self, argument_descriptor: ArgumentDescriptor) -> list:
        """
        Given the argument descriptor provided, tries to get the value
        associated with it. If not present, returns the default value included
        in the argument descriptor

        Parameters:
            argument_descriptor (ArgumentDescriptor): descriptor of the
            argument which value is needed.
        Returns:
            value(str): The value associated with the key present in the
            descriptor, the default value present in the descriptor if not
            found, casted to a list
        """
        logging.debug(f"ArgumentsParser.get_list(\"{argument_descriptor}\")")
        string = self.get(ArgumentDescriptor(argument_descriptor.key, ""))
        if string:
            string = string.strip()
            string = string[1:-1]
            value = list(string.split(","))
            value = list(map(str.strip, value))
        else:
            value = argument_descriptor.default_value
        return value

    def get_list_int(self, argument_descriptor: ArgumentDescriptor) -> list:
        """
        Given the argument descriptor provided, tries to get the value
        associated with it. If not present, returns the default value included
        in the argument descriptor

        Parameters:
            argument_descriptor (ArgumentDescriptor): descriptor of the
            argument which value is needed.
        Returns:
            value(str): The value associated with the key present in the
            descriptor, the default value present in the descriptor if not
            found, casted to an int list
        """
        logging.debug(f"ArgumentsParser.get_list_int(\"{argument_descriptor}\")")
        list_string = self.get_list(ArgumentDescriptor(argument_descriptor.key, []))
        if list:
            value = list(map(int, list_string))
        else:
            value = argument_descriptor.default_value
        return value

    @staticmethod
    def parse(string: str) -> dict:
        """
        Receives a string containing a list of arguments as a string, parses it
        into a dictionary using regular expressions
        """
        logging.debug(f"ArgumentsParser.parse(\"{string}\")")
        arguments = {}
        matches = re.findall(REGULAR_EXPRESSION, string)
        for match in matches:
            key = match[0]
            value = match[2]
            arguments[key] = value
        return arguments
