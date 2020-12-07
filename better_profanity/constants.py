# -*- coding: utf-8 -*-

from io import open
from json import load
from string import ascii_letters, digits

from .utils import get_complete_path_of_file

ALTERNATE_CHARS = {
    "a": ("*", "4", "@"),
    "i": ("*", "1", "l"),
    "o": ("*", "0", "@"),
    "u": ("*", "v"),
    "v": ("*", "u"),
    "l": ("1", "l"),
    "e": ("*", "3"),
    "s": ("$", "5"),
    "t": ("7",),
}

ALLOWED_CHARACTERS = set(ascii_letters)
ALLOWED_CHARACTERS.update(set(digits))
ALLOWED_CHARACTERS.update({'"', "'"})
for chars in ALTERNATE_CHARS.values():
    for ch in chars:
        ALLOWED_CHARACTERS.add(ch)

# Pre-load the unicode characters
with open(get_complete_path_of_file("alphabetic_unicode.json"), "r") as json_file:
    ALLOWED_CHARACTERS.update(load(json_file))
