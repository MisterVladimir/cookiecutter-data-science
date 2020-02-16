from setuptools import find_packages, setup

requirements = [
    "invoke",
    "loguru",
    "awscli",
]
requirments_dev = [
    "Sphinx",
    "pytest",
    "pytest-runner",
    "black",
    "pytest-black",
    "pytest-cov",
    "pylint",
    "pylint-mccabe",
    "twine",
]


if __name__ == "__main__":

    setup(
        name="{{ cookiecutter.project_slug }}",
        packages=find_packages(),
        install_requires=requirements,
        extras_require={"dev": requirments_dev,},
        version="0.1.0",
        description="{{ cookiecutter.description }}",
        author="{{ cookiecutter.author_name }}",
        license="{% if cookiecutter.open_source_license == 'MIT' %}MIT{% elif cookiecutter.open_source_license == 'BSD-3-Clause' %}BSD-3{% elif cookiecutter.open_source_license == 'GPLv3+' %}GPLv3+{% endif %}",
    )
