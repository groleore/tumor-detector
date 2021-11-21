from screens import *


def get_screen(name):
    for cls in Screen.__subclasses__():
        if cls.name() == name:
            return cls
