# Cookiecutter Data Science

_A logical, reasonably standardized, but flexible project structure for doing and sharing data science work._

The inspiration for this cookiecutter came from [drivendata](http://drivendata.github.io/cookiecutter-data-science/).


### Requirements to use the cookiecutter template:
-----------
 - Python 3.6+
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0

``` bash
$ pip install cookiecutter
```


### To start a new project, run:
------------

    cookiecutter https://github.com/MisterVladimir/cookiecutter-data-science.git


### The resulting directory structure
------------

The directory structure of your new project looks like this: 

```
.
├── {{ cookiecutter.project_slug }}     <- Source code for the project. This will be replaced by the
|                                          input provided by your answers to the cookiecutter prompts.
|                                          For example, by default, if your project is named "Project Name",
|                                          this will be renamed to "project_name".
│   ├── __init__.py
│   ├── data                            <- Scripts to download or process data
│   │   ├── __init__.py
│   │   └── main.py                     <- Command line interface (CLI) to download and process the data
│   ├── features                        <- Scripts to turn the data into features for modeling
│   │   ├── __init__.py                    
│   │   └── build.py
│   ├── models                          <- Scripts to train the models and use them to make inferences
│   │   ├── __init__.py
│   │   ├── predict.py
│   │   └── train.py
│   └── visualization                   <- Utilities for visualizing the results
│       ├── __init__.py
│       └── visualize.py
├── data                                <- Data used for training, testing and evaluation. By default the contents
|                                          are excluded from version control.
│   ├── external
│   ├── interim
│   ├── processed
│   └── raw
├── docs                                <- Documentation files and code used by Sphinx to generate
|                                          pretty documentation for developers.
├── LICENSE
├── Makefile                            <- Execute top-level commands, e.g. linting, running tests
├── models                              <- Models produced during training. By default the contents are
|                                          excluded from version control.
├── notebooks                           <- Jupyter notebooks as scratch files or for generating repots.
├── pyproject.toml                      <- Configuration of the project build system and other tools.
|                                          See https://www.python.org/dev/peps/pep-0518/ for details.
├── README.md                           <- Summary of the project, background, and installation and running instaructions
├── references                          
├── reports                             <- Human-readable text and supporting figures that summarize the results.
│   └── figures
├── requirements.txt                    <- List of version-pinned dependencies. Generate by doing `pip freeze > requirements.txt`
├── setup.py                            <- Enables building the source code and distributing it, e.g. as a `whl` file
├── pytest.ini                          <- Unit test configuration
└── test                                <- Directory containing the unit tests
```
