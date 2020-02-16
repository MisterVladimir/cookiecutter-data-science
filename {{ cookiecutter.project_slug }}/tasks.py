"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
# fmt: off
import invoke
from {{ cookiecutter.project_slug }} import monkeypatch

monkeypatch.fix_annotations()
# fmt: on

import pathlib
import platform
import webbrowser

from invoke import task
from packaging.version import parse, LegacyVersion, Version

ROOT_DIR = pathlib.Path(__file__).parent

SETUP_FILE = ROOT_DIR.joinpath("setup.py").resolve()
SOURCE_DIR = ROOT_DIR.joinpath("{{ cookiecutter.project_slug }}").resolve()
TEST_DIR = ROOT_DIR.joinpath("test").resolve()

#: Executables
BIN_DIR = ROOT_DIR.joinpath(".venv", "bin")
PYTHON = BIN_DIR.joinpath("python").resolve()
PYLINT = BIN_DIR.joinpath("pylint").resolve()
BLACK = BIN_DIR.joinpath("black").resolve()
PYTEST = BIN_DIR.joinpath("pytest").resolve()
SPHINX_BUILD = BIN_DIR.joinpath("sphinx-build").resolve()
TWINE = BIN_DIR.joinpath("twine").resolve()

#: Tests
PYTEST_CACHE_DIR = ROOT_DIR.joinpath(".pytest_cache")
TOX_DIR = ROOT_DIR.joinpath(".tox")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")

#: Documentation
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")

#: Raw data
DATA_DIR = ROOT_DIR.joinpath("data").resolve()


@task()
def s3(ctx, bucket, pull=False, push=False, profile=None, kwargs=""):
    """
    Synchronize data in /data with an s3 bucket.

    :param bucket:
        Name of the S3 bucket to synchronize with. Do not include the 's3://'.
    :param profile:
        AWS profile to use.
    :param pull:
        Download data from S3 to /data directory.
    :param push:
        Upload data from /data directory to S3.
    :param kwargs:
        Extra command-line command-line arguments to pass to the `s3 sync` command.
    """
    if profile:
        kwargs = f"{kwargs} --profile {profile}"

    if not (pull ^ push):
        raise RuntimeError("Only one of `push` or `pull` flags may be passed-in.")
    elif push:
        ctx.run(f"aws s3 sync {DATA_DIR} s3://{bucket}/data/ {kwargs}")
    elif pull:
        ctx.run(f"aws s3 sync s3://{bucket}/data/ {DATA_DIR}")


@task()
def format(ctx):
    """Automatically format the code."""
    ctx.run(f"{BLACK} {SOURCE_DIR} {TEST_DIR}")


@task()
def lint(ctx):
    """Lint code."""
    ctx.run(f"{PYLINT} --rcfile=.pylintrc {SOURCE_DIR} {TEST_DIR}")
    ctx.run(f"{BLACK} --check {SOURCE_DIR} {TEST_DIR}")


@task()
def test(ctx):
    """Run tests."""
    pty = platform.system() == "Linux"
    inifile = ROOT_DIR.joinpath("pytest.ini").resolve()
    ctx.run(f"{PYTEST} --c {inifile}", pty=pty)


@task()
def docs(ctx):
    """Generate documentation."""
    ctx.run(rf"{SPHINX_BUILD} -b html {DOCS_DIR} {DOCS_BUILD_DIR}")
    webbrowser.open(DOCS_INDEX.as_uri())


@task()
def clean_docs(ctx):
    """Clean up files from documentation builds."""
    ctx.run(rf"rm -rf {DOCS_BUILD_DIR}")


@task()
def clean_build(ctx):
    """Clean up files from package building."""
    ctx.run("rm -fr build/")
    ctx.run("rm -fr dist/")
    ctx.run("rm -fr .eggs/")
    ctx.run("find . -name '*.egg-info' -exec rm -fr {} +")
    ctx.run("find . -name '*.egg' -exec rm -f {} +")


@task()
def clean_python(ctx):
    """Clean up python file artifacts."""
    ctx.run("find . -name '*.py[co]' -exec rm -f {} +")
    ctx.run("find . -name '*~' -exec rm -f {} +")
    ctx.run("find . -name '__pycache__' -exec rm -rf {} +")


@task()
def clean_tests(ctx):
    """Clean up files from testing."""
    ctx.run(f"rm -rf {COVERAGE_FILE}")
    ctx.run(f"rm -rf {COVERAGE_DIR}")
    ctx.run(f"rm -rf {PYTEST_CACHE_DIR}")


@task(pre=[clean_build, clean_python, clean_tests, clean_docs])
def clean(ctx):
    """Run all clean sub-tasks."""
    pass


def _as_version_object(version) -> Version:
    """
    Convert a version string to a Version object.

    :raise ValueError:
        The passed-in version does not conform to PEP440.
    """
    version = parse(version)
    if isinstance(version, LegacyVersion):
        raise ValueError("`version` argument does not conform to PEP440.")

    return version


@task()
def tag(ctx, version) -> None:
    """
    Add a git tag to the current commit.

    :param version:
        Semantic version with which to tag.
    """
    ctx.run("git checkout origin/develop")
    _version = _as_version_object(version=version)
    ctx.run(f'git tag v{_version} -m "v{_version}"')


@task(pre=[clean, ])
def dist(ctx):
    """Build source and wheel packages."""
    ctx.run(f"{PYTHON} {SETUP_FILE} sdist")
    ctx.run(f"{PYTHON} {SETUP_FILE} bdist_wheel")


@task(pre=[clean, dist, ])
def release(ctx):
    """Release the package to PyPi."""
    ctx.run(f"{TWINE} upload dist/*")
