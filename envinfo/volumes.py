from os import popen
from re import findall, MULTILINE
from string import ascii_uppercase
from ctypes import windll


def get_volumes():
    """Get all drives and mounted volumes"""
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return ['{0}:\\'.format(d) for d in drives]


def get_drives():
    """Get mounted volumnes"""
    return findall(r"[A-Z]+:.*$", popen("mountvol /").read(), MULTILINE)
