# -*- coding: utf-8 -*-

"""
"Hello World" function used by the smoke test (see test/test_hello_world.py).

Developers should delete this file after running it once (and it passes).
"""

def say_hello(name: str) -> str:
    """
    Greet someone in English.

    :param name:
        Name of the person to greet.
    :return:
        The greeting.
    """
    return f"Hello {name}!"
