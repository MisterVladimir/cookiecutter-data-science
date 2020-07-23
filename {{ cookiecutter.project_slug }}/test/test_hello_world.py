# -*- coding: utf-8 -*-

"""
A smoke test for generating the repo from the cookiecutter.

Developers should delete this file after running it once (and it passes).
"""
from {{ cookiecutter.project_slug }}.hello_world import say_hello

def test_say_hello() -> None:
    """
    Assert that `say_hello` returns exactly the expected string.
    """
    # Arrange

    # Act
    result = say_hello("cookiecutter")

    # Assert
    assert result == "Hello cookiecutter!"
