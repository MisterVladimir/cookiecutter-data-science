# -*- coding: utf-8 -*-

"""Script to execute after generating the project from the cookiecutter."""

import pathlib
import re
import sys
from typing import List


def _load_file_contents(path: pathlib.Path) -> str:
    """Return the contents of a file."""
    with path.open("r") as fp:
        return fp.read()


def _contains_curly_braces(value: str) -> bool:
    """Return whether the argument contains curly braces."""
    # {% raw %}  escape cookiecutter/jinja2 template
    curly_brace_re = re.compile(r"{{.*?}}")
    percent_curly_brace_re = re.compile(r"{%.*?%}")
    # {% endraw %}
    return bool(curly_brace_re.search(value) or percent_curly_brace_re.search(value))


def _get_all_files(root: pathlib.Path) -> List[pathlib.Path]:
    """Walk the directory tree and return all the Python modules."""
    return [path for path in root.glob("**/*") if path.is_file()]


def _get_all_directories(root: pathlib.Path) -> List[pathlib.Path]:
    """Walk the directory tree and return all the folders."""
    all_files_and_folders = root.glob("**/*")
    return [path for path in all_files_and_folders if path.is_dir()]


def _is_python_path_valid(name: str) -> bool:
    """
    Return whether `name` is a valid Python package or module name.

    :param name:
        Name of the folder or Python module.
    """
    valid_module_re = re.compile(r"^[_a-zA-Z][_a-zA-Z0-9]+(\.py)?$")
    return bool(valid_module_re.match(name))


def _get_extra_gitignore_text() -> str:
    """
    Return the text to append to the `.gitignore` file.
    """
    return """
    # Data to exclude from version control.
    data/
    
    # Models produced by training.
    models/
    """


def main():
    """Body of the pot-gen script."""
    project_root = pathlib.Path(".")

    # Check that the project was generated correctly.
    all_package_dir = _get_all_directories(project_root)

    for directory in all_package_dir:
        if directory.joinpath("__init__.py").exists() and not _is_python_path_valid(
            directory.name
        ):
            print(f"{directory.name} is not a valid Python package name.")
            sys.exit(1)

    all_generated_files = _get_all_files(project_root)
    for file in all_generated_files:
        if file.match("*.py") and not _is_python_path_valid(file.name):
            print(f"{file.name} is not a valid Python module name.")
            sys.exit(1)

        file_contents = _load_file_contents(file)
        if _contains_curly_braces(file_contents):
            print(f"Jinja template was not correctly filled in {file.resolve()}")
            sys.exit(1)

    # Add data and raw model files to .gitignore
    with open(".gitignore", "w") as fp:
        fp.write(_get_extra_gitignore_text())


if __name__ == '__main__':
    main()
