"""
Integration tests that create a project from the `cookiecutter-data-science`
repo and test whether the file names and templates have been correctly generated.
"""

import pathlib
import shutil
import subprocess
from typing import Callable, Union

import attr
import pytest
from cookiecutter import main


@attr.attrs(slots=True)
class CookieCutterTestConfig:
    """
    Container for arguments to the `cookiecutter cookiecutter-data-science`
    shell command.
    """

    project_name = attr.ib(type=str)
    repo_name = attr.ib(type=str)
    package_name = attr.ib(type=str)
    author_name = attr.ib(type=str)
    open_source_license = attr.ib(
        type=str,
        validator=attr.validators.in_(["MIT", "BSD-3-Clause", "No license file"]),
    )


@pytest.fixture(scope="session")
def assert_no_curly_braces() -> Callable[[Union[str, pathlib.Path]], bool]:
    """Return a function that checks for curly braces in a file."""

    def _assert_no_curly_braces(filepath: Union[str, pathlib.Path]) -> bool:
        """Return whether the passed-in file contains curly braces."""
        with open(filepath, "r") as f:
            file_contents = f.read()

        template_strings = ["{{", "}}", "{%", "%}"]

        template_strings_in_file = [s in file_contents for s in template_strings]
        return not any(template_strings_in_file)

    return _assert_no_curly_braces


@pytest.fixture(scope="session")
def cookiecutter_call_args() -> CookieCutterTestConfig:
    """
    Return arguments with which to call the `cookiecutter cookiecutter-data-science`
    shell command in the tests.
    """
    return CookieCutterTestConfig(
        project_name="Project Under Test",
        repo_name="project-under-test",
        package_name="project_under_test",
        author_name="Vladimir Shteyn",
        open_source_license="BSD-3-Clause",
    )


@pytest.fixture(scope="session")
def cookiecutter_out_dir(
    tmpdir_factory, cookiecutter_call_args: CookieCutterTestConfig,
) -> str:
    """
    Execute the `cookiecutter cookiecutter-data-science` shell command and return
    its parent directory.
    """
    path_of_current_file = pathlib.Path(__file__)
    repo_dir = path_of_current_file.parents[1]

    _cookiecutter_out_dir = tmpdir_factory.mktemp(basename="tmp")

    main.cookiecutter(
        str(repo_dir),
        no_input=True,
        extra_context=attr.asdict(cookiecutter_call_args),
        output_dir=_cookiecutter_out_dir,
    )

    yield _cookiecutter_out_dir

    # cleanup after
    shutil.rmtree(_cookiecutter_out_dir)


@pytest.fixture(scope="session")
def expected_cookiecutter_repo_dir(
    cookiecutter_out_dir: str, cookiecutter_call_args: CookieCutterTestConfig
) -> pathlib.Path:
    """
    Return the expected path to the repository produced by
    `cookiecuter cookiecutter-data-science`.
    """
    cookiecutter_out_dir = pathlib.Path(cookiecutter_out_dir)
    return cookiecutter_out_dir.joinpath(cookiecutter_call_args.repo_name)


@pytest.fixture(scope="session")
def expected_cookiecutter_package_dir(
    expected_cookiecutter_repo_dir: pathlib.Path,
    cookiecutter_call_args: CookieCutterTestConfig,
) -> pathlib.Path:
    """
    Return the expected path to the Python package produced by
    `cookiecuter cookiecutter-data-science`.
    """
    return expected_cookiecutter_repo_dir.joinpath(cookiecutter_call_args.package_name)


@pytest.fixture(scope="session")
def call_setup_module(
    expected_cookiecutter_repo_dir: pathlib.Path,
    cookiecutter_call_args: CookieCutterTestConfig,
) -> Callable[[str], str]:
    """
    Return a function that executes the `setup.py` file produced by the
    `cookiecutter cookiecutter-data-science` shell command.
    """
    setup_module_path = expected_cookiecutter_repo_dir.joinpath("setup.py")

    def _call_setup_module(option: str) -> str:
        """
        Execute the `setup.py` file produced by the
        `cookiecutter cookiecutter-data-science` shell command.

        :param option:
            Flag to pass to the shell command.
        :return:
            Result of stdout as a string.
        :raise RuntimeError:
            Raise RuntimeError if executing `setup.py` returns with a nonzero
            status code.
        """
        args = ["python", str(setup_module_path), f"--{option}"]
        result = subprocess.run(args, check=True, capture_output=True)
        if result.returncode == 0:
            return result.stdout.decode("utf-8").strip()

        raise RuntimeError(
            f"Returned status code: {result.returncode}, stderr: {result.stderr}"
        )

    return _call_setup_module


@pytest.fixture(
    scope="session",
    params=["Makefile", "requirements.txt", "LICENSE"],
    ids=["makefile", "requirements", "license"],
)
def path_of_generated_file(
    request, expected_cookiecutter_repo_dir: pathlib.Path
) -> pathlib.Path:
    """
    Standard Python files that executing `cookiecutter cookiecutter-data-science`
    should always produce.
    """
    return expected_cookiecutter_repo_dir.joinpath(request.param)


def test_cookiecutter_output_repo_name(
    expected_cookiecutter_repo_dir: pathlib.Path,
) -> None:
    """
    Assert that executing `cookiecutter cookiecutter-data-science` produced a
    repository with the correct name.
    """
    # Arrange and Act performed in fixtures
    # Assert
    assert expected_cookiecutter_repo_dir.exists()


def test_cookiecutter_output_package_name(
    expected_cookiecutter_package_dir: pathlib.Path,
) -> None:
    """
    Assert that executing `cookiecutter cookiecutter-data-science` produced a
    repository with the correct name.
    """
    # Arrange and Act performed in fixtures
    # Assert
    assert expected_cookiecutter_package_dir.exists()


def test_author(
    call_setup_module: Callable[[str], str],
    cookiecutter_call_args: CookieCutterTestConfig,
) -> None:
    """Test whether the correct author name was set."""
    # Arrange
    # Act
    result_of_test = call_setup_module("author")

    # Assert
    assert result_of_test == cookiecutter_call_args.author_name


def test_version_string(call_setup_module: Callable[[str], str]):
    """Test whether the version string was correctly set."""
    # Arrange performed in fixtures.
    # Act
    result_of_test = call_setup_module("version")
    assert result_of_test == "0.1.0"


def test_license_type(call_setup_module: Callable[[str], str]) -> None:
    """Test whether the correct license was set."""
    # Arrange performed in fixtures.
    # Act
    result_of_test = call_setup_module("license")
    # Assert
    assert result_of_test == "BSD-3"


def test_no_curlies(
    path_of_generated_file: pathlib.Path, assert_no_curly_braces,
) -> None:
    """Test that the generated template files were substituted with values."""
    # Arrange and Act performed in fixtures
    # Assert
    assert assert_no_curly_braces(path_of_generated_file)
