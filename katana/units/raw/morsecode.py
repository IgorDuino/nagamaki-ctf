"""
Unit to decode Morsecode 

This unit will attempt to read data from Morsecode, both in the International 
sound mapping as well as the text representation with dots and dashes.
"""

#!/usr/bin/env python3
import string
from typing import Any

import regex as re

from katana.unit import RegexUnit


class Unit(RegexUnit):

    PRIORITY = 30
    """
    Priority works with 0 being the highest priority, and 100 being the 
    lowest priority. 50 is the default priorty. This unit has a moderate
    priority
    """

    # Unit groups
    GROUPS = ["raw", "decode", "morsecode"]
    """
    These are "tags" for a unit. Considering it is a Raw unit, "raw"
    is included, as well as the tag "decode", and the unit name "morsecode".
    """

    # This matches international or traditional morse code strings of at least 4 characters
    PATTERN = re.compile(
        rb"((((dit|dah|di)-?)+)|([.\-]+))( ((((dit|dah|di)-?)+)|([.\-]+))){3,}",
        re.DOTALL | re.MULTILINE,
    )

    def evaluate(self, match):
        """
        Evaluate the target. Translate any morsecode in the target and
        to its English representation and recurse on any newfound information.

        :param match: A match returned by the ``RegexUnit``.

        :return: None. This function should not return any data.
        """

        international_morse_code_mapping = {
            b"di-dah": "A",
            b"dah-di-di-dit": "B",
            b"dah-di-dah-dit": "C",
            b"dah-di-dit": "D",
            b"dit": "E",
            b"di-di-dah-dit": "F",
            b"dah-dah-dit": "G",
            b"di-di-di-dit": "H",
            b"di-dit": "I",
            b"di-dah-dah-dah": "J",
            b"dah-di-dah": "K",
            b"di-dah-di-dit": "L",
            b"dah-dah": "M",
            b"dah-dit": "N",
            b"dah-dah-dah": "O",
            b"di-dah-dah-dit": "P",
            b"dah-dah-di-dah": "Q",
            b"di-dah-dit": "R",
            b"di-di-dit": "S",
            b"dah": "T",
            b"di-di-dah": "U",
            b"di-di-di-dah": "V",
            b"di-dah-dah": "W",
            b"dah-di-di-dah": "X",
            b"dah-di-dah-dah": "Y",
            b"dah-dah-di-dit": "Z",
            b"dah-dah-dah-dah-dah": "0",
            b"di-dah-dah-dah-dah": "1",
            b"di-di-dah-dah-dah": "2",
            b"di-di-di-dah-dah": "3",
            b"di-di-di-di-dah": "4",
            b"di-di-di-di-dit": "5",
            b"dah-di-di-di-dit": "6",
            b"dah-dah-di-di-dit": "7",
            b"dah-dah-dah-di-dit": "8",
            b"dah-dah-dah-dah-dit": "9",
            b"di-dah-di-dah": "??",
            b"di-dah-dah-di-dah": "??",
            b"dah-dah-dah-dah": "Ch",
            b"di-di-dah-di-dit": "??",
            b"dah-dah-di-dah-dah": "??",
            b"dah-dah-dah-dit": "??",
            b"di-di-dah-dah": "??",
            b"di-dah-di-di-dit": "&",
            b"di-dah-dah-dah-dah-dit": "'",
            b"di-dah-dah-di-dah-dit": "@",
            b"dah-di-dah-dah-di-dah": ")",
            b"dah-di-dah-dah-dit": "(",
            b"dah-dah-dah-di-di-dit": ":",
            b"dah-dah-di-di-dah-dah": ",",
            b"dah-di-di-di-dah": "=",
            b"dah-di-dah-di-dah-dah": "!",
            b"di-dah-di-dah-di-dah": ".",
            b"dah-di-di-di-di-dah": "-",
            b"di-dah-di-dah-dit": "+",
            b"di-dah-di-di-dah-dit": '"',
            b"di-di-dah-dah-di-dit": "?",
            b"dah-di-di-dah-dit": "/",
        }

        morse_alphabet = {
            b".-": "A",
            b"-...": "B",
            b"-.-.": "C",
            b"-..": "D",
            b".": "E",
            b"..-.": "F",
            b"--.": "G",
            b"....": "H",
            b"..": "I",
            b".---": "J",
            b"-.-": "K",
            b".-..": "L",
            b"--": "M",
            b"-.": "N",
            b"---": "O",
            b".--.": "P",
            b"--.-": "Q",
            b".-.": "R",
            b"...": "S",
            b"-": "T",
            b"..-": "U",
            b"...-": "V",
            b".--": "W",
            b"-..-": "X",
            b"-.--": "Y",
            b"--..": "Z",
            b"-----": "0",
            b"--..--": ",",
            b".----": "1",
            b".-.-.-": ".",
            b"..---": "2",
            b"..--..": "?",
            b"...--": "3",
            b"-.-.-.": ";",
            b"....-": "4",
            b"---...": ":",
            b".....": "5",
            b".----.": "'",
            b"-....": "6",
            b"-....-": "-",
            b"--...": "7",
            b"-..-.": "/",
            b"---..": "8",
            b"-.--.": "(",
            b"----.": "9",
            b"-.--.-": ")",
            b"/": " ",
            b"..--.-": "_",
            b" ": "/",
            b"-...-": "=",
        }

        morse = match.group()
        result = []

        for letter in morse.split(b" "):
            if letter in international_morse_code_mapping:
                result.append(international_morse_code_mapping[letter])
            elif letter in morse_alphabet:
                result.append(morse_alphabet[letter])

        result = "".join(result).strip()

        if len(result):
            self.manager.register_data(self, result)
